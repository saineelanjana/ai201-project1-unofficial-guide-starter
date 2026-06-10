"""
query.py

Implements the grounded generation layer:
  - Retrieves relevant chunks from the vector store
  - Enforces grounding by passing context explicitly to the LLM
  - Programmatically extracts and attributes sources
  - Returns structured response: {answer, sources, retrieved_chunks}

The system prompt is designed to ENFORCE grounding, not just suggest it:
  - Explicitly forbids drawing on training knowledge
  - Requires citing sources for every claim
  - Instructs the model to say "I don't have enough information" if context is insufficient
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import vector store and LLM client
from vector_store import VectorStore

try:
    from groq import Groq
except ImportError:
    print("ERROR: groq is required. Install with: pip install groq")
    raise

try:
    from dotenv import load_dotenv
except ImportError:
    print("WARNING: python-dotenv not found. Set GROQ_API_KEY environment variable directly.")
    load_dotenv = None


# ============================================================================
# CONFIGURATION
# ============================================================================

# Load .env file if it exists (optional)
if load_dotenv:
    load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable not set. "
        "Set it in .env or in your shell: export GROQ_API_KEY=..."
    )

# Model to use (Groq's free-tier, OpenAI-compatible)
MODEL = "llama-3.3-70b-versatile"

# Retrieval params
RETRIEVE_K = 4
RETRIEVAL_LOG_PATH = "retrieval_log.json"


# ============================================================================
# GROUNDING SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are a helpful assistant for an OMSCS (Georgia Tech Online Master of Science in Computer Science) knowledge base.

CRITICAL GROUNDING RULE: You must answer ONLY using the information provided in the documents below. 
If the documents contain relevant information, use it to answer with citations.
If the documents do NOT contain enough information to answer the question, you MUST respond with:
"I don't have enough information on that topic in the available documents."

DO NOT:
- Draw on your general training knowledge
- Make up facts or infer beyond what the documents state
- Suggest plausible-sounding answers that aren't in the documents
- Provide general advice that isn't grounded in the provided context

DO:
- Quote or paraphrase specific passages from the documents
- Clearly cite which documents your answer comes from
- Acknowledge when information is contradictory or from multiple sources
- Say you don't know if the context doesn't cover the question

Remember: Your role is to be a faithful conduit of the document knowledge, not a general-purpose assistant."""


# ============================================================================
# RETRIEVAL LOGGING
# ============================================================================

def log_retrieval(query: str, retrieved_chunks: List[Dict[str, Any]],
                  response: str, sources: List[str]) -> None:
    """Log retrieval and generation for audit trail."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "retrieved_chunks_count": len(retrieved_chunks),
        "retrieved_sources": list(set(s["metadata"]["source"] for s in retrieved_chunks)),
        "cited_sources": sources,
        "response_length": len(response),
        "response_preview": response[:200] + "..." if len(response) > 200 else response,
    }

    # Append to or create log file
    entries = []
    if os.path.exists(RETRIEVAL_LOG_PATH):
        try:
            with open(RETRIEVAL_LOG_PATH, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []

    entries.append(log_entry)
    with open(RETRIEVAL_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


# ============================================================================
# CORE QUERY ENGINE
# ============================================================================

class GroundedQueryEngine:
    """Query engine that enforces grounding in retrieved context."""

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.store = vector_store or VectorStore()
        self.client = Groq(api_key=GROQ_API_KEY)

    def format_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks into a context block for the prompt."""
        if not retrieved_chunks:
            return "No documents were retrieved."

        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            source = chunk["metadata"].get("source", "unknown")
            text = chunk["document"]
            context_parts.append(f"[Source {i}: {source}]\n{text}")

        return "\n\n---\n\n".join(context_parts)

    def extract_unique_sources(self, retrieved_chunks: List[Dict[str, Any]]) -> List[str]:
        """Extract unique source file paths from retrieved chunks."""
        sources = set()
        for chunk in retrieved_chunks:
            source = chunk["metadata"].get("source")
            if source:
                sources.add(source)
        return sorted(list(sources))

    def query(self, question: str, k: int = RETRIEVE_K) -> Dict[str, Any]:
        """
        End-to-end query with grounding enforcement.

        Returns:
            {
                "answer": str,           # LLM response grounded in context
                "sources": List[str],    # Unique source files used
                "retrieved_chunks": List[Dict],  # Full retrieval results (for inspection)
                "grounding_status": str  # "success" or "potential_grounding_failure"
            }
        """
        # Step 1: Retrieve context
        print(f"🔍 Retrieving context for: {question[:60]}...")
        retrieved_chunks = self.store.retrieve(question, k=k)
        sources = self.extract_unique_sources(retrieved_chunks)

        if not retrieved_chunks:
            return {
                "answer": "I don't have enough information on that topic in the available documents.",
                "sources": [],
                "retrieved_chunks": [],
                "grounding_status": "no_context",
            }

        # Step 2: Format context block
        context = self.format_context(retrieved_chunks)

        # Step 3: Construct prompt with grounding enforcement
        user_message = f"""Please answer the following question using ONLY the provided documents.
If the documents don't contain enough information, say so explicitly.

QUESTION: {question}

DOCUMENTS:
{context}

ANSWER (grounded in the above documents only):"""

        # Step 4: Call Groq LLM with system prompt enforcing grounding
        print(f"💭 Querying {MODEL} with {len(retrieved_chunks)} retrieved chunks...")
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                temperature=0.4,  # Lower temperature for more deterministic, grounded responses
                max_tokens=1024,
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return {
                "answer": f"Error querying LLM: {str(e)}",
                "sources": sources,
                "retrieved_chunks": retrieved_chunks,
                "grounding_status": "error",
            }

        # Step 5: Audit grounding by checking answer length relative to context
        # (This is a heuristic; perfect grounding detection is hard without semantic analysis)
        grounding_status = "success"
        if len(answer) < 50 and not any(phrase in answer.lower() for phrase in
                                        ["don't have", "enough information", "not found", "unclear"]):
            # Very short answer that doesn't acknowledge lack of info suggests possible hallucination
            grounding_status = "warning_short_answer"

        # Step 6: Log for audit trail
        log_retrieval(question, retrieved_chunks, answer, sources)

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": retrieved_chunks,
            "grounding_status": grounding_status,
        }


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def ask(question: str) -> Dict[str, Any]:
    """Simple wrapper to query with a single question."""
    engine = GroundedQueryEngine()
    return engine.query(question)


# ============================================================================
# TESTING
# ============================================================================

def test_grounded_generation():
    """Test the grounding enforcement on 3 queries:
       - 2 queries the system should answer from documents
       - 1 query the system should admit it doesn't have info for
    """
    engine = GroundedQueryEngine()

    test_queries = [
        # Query 1: Should have good document coverage
        ("What preparatory CS courses should a non-traditional applicant take for OMSCS admissions?", True),

        # Query 2: Should have document coverage from reviews
        ("What are the best courses to pair with CS 6200 (GIOS) for someone working full-time?", True),

        # Query 3: Likely NOT in documents (test grounding failure detection)
        ("What is the current CEO of Google and when were they appointed?", False),
    ]

    for i, (query, expect_in_docs) in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {query[:60]}...")
        print(f"Expected in documents: {expect_in_docs}")
        print(f"{'='*70}")

        result = engine.query(query)
        answer = result["answer"]
        sources = result["sources"]
        grounding = result["grounding_status"]

        print(f"\n📄 SOURCES ({len(sources)}):")
        for src in sources:
            print(f"  • {src}")

        print(f"\n💬 ANSWER:")
        print(f"  {answer[:300]}..." if len(answer) > 300 else f"  {answer}")

        print(f"\n🎯 GROUNDING STATUS: {grounding}")

        # Heuristic check: if expect_in_docs=False but we got a real answer, that's a grounding failure
        if not expect_in_docs:
            if "don't have" not in answer.lower() and "not found" not in answer.lower():
                print("⚠️  POTENTIAL GROUNDING FAILURE: Got an answer when documents likely don't cover this!")
            else:
                print("✓ GOOD: System correctly admitted lack of information")

        print(f"\n📊 Retrieved {len(result['retrieved_chunks'])} chunks")


if __name__ == "__main__":
    test_grounded_generation()

