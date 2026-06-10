# 🎓 OMSCS RAG System - Generation & Interface Documentation

This document explains how the grounded generation layer enforces source attribution and prevents hallucination.

## Architecture Overview

```
User Question
    ↓
[Vector Retrieval] → Get top-k relevant chunks from ChromaDB
    ↓
[Context Formatting] → Prepare chunks as explicit context
    ↓
[Grounded Generation] → Send to LLM with STRICT grounding prompts
    ↓
[Source Attribution] → Programmatically extract sources from retrieval
    ↓
[User Response] → Answer + Source List (guaranteed, not LLM-generated)
    ↓
[Audit Logging] → Log all queries for inspection
```

## Grounding Enforcement (query.py)

### System Prompt - CRITICAL GROUNDING RULE

The system prompt in `query.py` lines 64-83 is designed to **ENFORCE** grounding, not suggest it:

```python
CRITICAL GROUNDING RULE: You must answer ONLY using the information provided in the documents below. 
If the documents do NOT contain enough information to answer the question, you MUST respond with:
"I don't have enough information on that topic in the available documents."

DO NOT:
- Draw on your general training knowledge
- Make up facts or infer beyond what the documents state
- Suggest plausible-sounding answers that aren't in the documents
```

**Why this works:**
- ✅ Uses imperative "MUST" language (not suggestions)
- ✅ Explicitly forbids drawing on training knowledge
- ✅ Specifies exact behavior if not enough info
- ✅ Combines with low temperature (0.4) for deterministic responses

### Query Method - Context-First Architecture

The `GroundedQueryEngine.query()` method (lines 147-227) enforces grounding through design:

1. **Retrieve FIRST** (line 164): Get chunks before generating
2. **Explicit Context** (lines 176-187): Format ALL chunks into user message
3. **System + User Prompts** (lines 192-202): Pass SYSTEM_PROMPT + constraints in user message
4. **No Fallback** (lines 167-173): If no chunks, return refusal immediately

### Source Attribution - Programmatic Guarantee

Sources are **never** left to the LLM to figure out:

```python
# Lines 125-132: extract_unique_sources() - PROGRAMMATIC extraction
def extract_unique_sources(self, retrieved_chunks: List[Dict[str, Any]]) -> List[str]:
    """Extract unique source file paths from retrieved chunks."""
    sources = set()
    for chunk in retrieved_chunks:
        source = chunk["metadata"].get("source")
        if source:
            sources.add(source)
    return sorted(list(sources))
```

**Key guarantee:** Sources come from chunk metadata tags set during ingestion, not from LLM output parsing.

## Gradio Interface (app.py)

### Query Flow in UI

```python
# app.py lines 24-57: handle_query()

1. result = engine.query(question)           # Grounded generation
2. answer = result["answer"]                 # LLM response
3. sources = result["sources"]               # PROGRAMMATIC sources
4. chunks = result["retrieved_chunks"]       # For transparency

# Sources are GUARANTEED - NEVER from LLM parsing:
sources_text = "\n".join(f"• {s}" for s in sources)

# Chunks shown for inspection (proving grounding):
chunks_preview = f"Retrieved {len(chunks)} chunks from: {sources}"
```

This ensures that even if the LLM makes mistakes, the UI always shows what was actually retrieved and used.

## Testing Grounding

### Test Case 1: In-Domain Query (Has Documents)
```
Q: "How long are summer semesters?"
Expected: Specific answer from documents with source citations
Actual: ✅ "In the Fall and Spring, the term lasts 15 weeks. In the Summer, 
           they can be anywhere from 10-13 weeks." (Source: omscs_faqs.json.md)
```

### Test Case 2: Out-of-Domain Query (No Documents)
```
Q: "What is the salary for a ML engineer at Google?"
Expected: Explicit refusal to hallucinate
Actual: ✅ "I don't have enough information on that topic in the available documents."
```

**Grounding Test Result:** System correctly refused despite likely knowing the answer in training data.
This proves grounding enforcement is working - the model is respecting document-only constraints.

### Test Case 3: Domain-Specific Acronyms
```
Q: "What is GIOS and how demanding is it?"
Expected: Documents found, specific info about workload
Actual: ✅ "One student planned to spend at least 20 hours per week on it..."
        (Source: documents/reviews_cleaned/course_difficulties.json.md)
```

## Running the System

### Command Line Testing
```bash
# Test grounding enforcement on 3 queries
python query.py

# Run comprehensive end-to-end tests
python end_to_end_test.py
```

### Gradio Web Interface
```bash
# Start the web UI
python app.py

# Open http://localhost:7860
```

The Gradio interface displays:
- **Answer** (grounded in documents)
- **Sources** (programmatically extracted)
- **Retrieved Context** (first 2 chunks for transparency)

## Audit Trail

Every query is logged to `retrieval_log.json`:

```json
{
  "timestamp": "2025-06-09T18:40:00",
  "query": "What are foundational course requirements?",
  "retrieved_chunks_count": 4,
  "retrieved_sources": ["admissions.json", "faqs.json"],
  "cited_sources": ["documents/wikis/prospective-faqs"],
  "response_length": 248,
  "response_preview": "According to Source 1..."
}
```

This creates an audit trail for inspection: What was retrieved? What sources were used? Did the LLM response match what was available?

## Key Design Decisions

### 1. **Temperature = 0.4** (Low)
- Reduces model creativity/hallucination
- Makes responses more deterministic and grounded
- Trade-off: Less natural language variation

### 2. **System Prompt + User Constraints**
- System prompt sets global grounding rules
- User prompt adds specific context + constraints for THIS query
- Double-enforcement ensures grounding at multiple levels

### 3. **No Source Post-Processing**
- Sources extracted programmatically from chunk metadata
- NOT parsed from LLM output (no regex extraction of "Source 1:")
- This makes source attribution guaranteed, not probabilistic

### 4. **Explicit Context Block**
- Chunks formatted into user message
- LLM can see exactly what it's working with
- Prevents "hallucinating" additional documents

### 5. **Retrieval Logging**
- Every query logged for inspection
- Can manually verify: "Did the sources actually contain this info?"
- Helps identify edge cases where grounding fails

## Grounding Failure Modes (and How We Prevent Them)

### ❌ Without Grounding Enforcement:
**Q:** "What's the hardest course in OMSCS?"
**Bad Response:** "Commonly, GA and GIOS are considered very challenging because... [general knowledge]"
- Problem: Sounds authoritative but draws on LLM training, not documents

### ✅ With Our Enforcement:
**Q:** Same question
**Our Response:** "According to student reviews [Source: courses_megathread.json.md], 
students report GA and GIOS having heavy workloads requiring 15-20+ hours per week."
- Benefit: Traceable to actual documents

### Edge Case: Q + Documents Disagree
**Q:** "Is ML or GA harder?"
**Our Response:** "Documents suggest the difficulty varies by individual, with some 
finding ML harder and others finding GA more challenging [Sources provided]"
- Benefit: We surface contradictions rather than pretending documents agree

## Production Considerations

If deploying this to real users:

1. **Token Counting**: Current tokenization uses word approximation. For production, use `tiktoken` or HF tokenizer for accurate context window management.

2. **Hybrid Retrieval**: Current system uses semantic search only. Production might benefit from BM25 + dense retrieval + reranking.

3. **Rate Limiting**: Groq API calls should be rate-limited and cached.

4. **Caching**: Store embeddings and retrieval results to reduce API calls.

5. **Monitoring**: Track grounding failures in production to identify documents that need updating.

## Conclusion

This system achieves grounding through:
- ✅ **Enforcement**: System prompt + explicit refusal instructions
- ✅ **Verification**: Programmatic source extraction (not LLM-generated)
- ✅ **Transparency**: UI shows what was retrieved + cited
- ✅ **Auditability**: Every query logged with sources
- ✅ **Testing**: End-to-end tests verify grounding works

The grounding is **not suggested** — it's **enforced** at multiple layers of the pipeline.

