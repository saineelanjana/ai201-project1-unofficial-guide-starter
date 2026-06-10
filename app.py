"""
app.py

Gradio web interface for the OMSCS RAG system.
Provides a user-friendly query interface with:
  - Question input box
  - Answer output (grounded in retrieved documents)
  - Source attribution (which documents were used)
  - Optional: Retrieved chunks for transparency/debugging

Run with: python app.py
Then open http://localhost:7860
"""

import gradio as gr
from query import GroundedQueryEngine
import os


# Initialize the query engine once
engine = GroundedQueryEngine()


def handle_query(question: str) -> tuple:
    """
    Process a user question and return:
      - answer: The grounded response
      - sources_text: Formatted list of source files
      - chunks_text: Preview of retrieved chunks (for transparency)
    """
    if not question or not question.strip():
        return "", "No sources available", "Submit a question to see retrieved context."

    result = engine.query(question)

    answer = result["answer"]
    sources = result["sources"]
    retrieved_chunks = result["retrieved_chunks"]

    # Format sources
    if sources:
        sources_text = "Retrieved from:\n" + "\n".join(f"• {s}" for s in sources)
    else:
        sources_text = "No sources retrieved"

    # Format chunks for transparency (show first 2 with snippets)
    if retrieved_chunks:
        chunks_preview = f"📦 Retrieved {len(retrieved_chunks)} chunks:\n\n"
        for i, chunk in enumerate(retrieved_chunks[:2], 1):
            src = chunk["metadata"].get("source", "unknown")
            doc = chunk["document"]
            snippet = doc[:150].replace("\n", " ")
            chunks_preview += f"[{i}] {src}\n{snippet}...\n\n"
    else:
        chunks_preview = "No chunks retrieved"

    return answer, sources_text, chunks_preview


# Build the Gradio interface using gr.Blocks for better control
with gr.Blocks(title="OMSCS unofficial guide - RAG Query System", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
# 🎓 OMSCS Unofficial Guide - RAG Query System
    
Ask me anything about:
- **Admissions strategies** for Georgia Tech's OMSCS
- **Course selection & pairings** to manage workload
- **Academic policies** and foundational requirements
- **Student experiences** and burnout management
    
I'll answer using only the information from OMSCS student reviews, official GT documentation, and community guides.
All answers are grounded in retrieved documents — see sources below each response.
""")

    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="Ask a question",
                placeholder="E.g., What courses should I pair with GIOS if I work full-time?",
                lines=2,
                scale=1,
            )
            submit_btn = gr.Button("Ask", variant="primary", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("*Click Ask or press Enter*")

    with gr.Row():
        with gr.Column():
            answer_output = gr.Textbox(
                label="Answer (grounded in retrieved documents)",
                lines=8,
                interactive=False,
            )

    with gr.Row():
        with gr.Column():
            sources_output = gr.Textbox(
                label="Sources",
                lines=3,
                interactive=False,
            )

        with gr.Column():
            chunks_output = gr.Textbox(
                label="Retrieved Context (first 2 chunks)",
                lines=3,
                interactive=False,
            )

    gr.Markdown("""
### About Grounding
This system is designed to answer **only** from the provided documents. 
If retrieved documents don't contain enough information, it will say so explicitly.
Each answer includes source attribution to show which documents were used.

### Example Queries
- "What are the foundational course requirements?"
- "How does summer semester compare to fall/spring?"
- "Which specializations are most popular?"
- "How much time does CS 6200 actually take per week?"
    """)

    # Wire up button and text input
    submit_btn.click(
        handle_query,
        inputs=[question_input],
        outputs=[answer_output, sources_output, chunks_output],
    )

    # Also allow pressing Enter in the text box
    question_input.submit(
        handle_query,
        inputs=[question_input],
        outputs=[answer_output, sources_output, chunks_output],
    )


if __name__ == "__main__":
    print("🚀 Starting OMSCS RAG interface...")
    print("📍 Open http://localhost:7860 in your browser")
    print("🛑 Press Ctrl+C to stop")
    demo.launch()

