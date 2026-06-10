# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

> * I chose the domain "Unofficial Guide to Admissions, Course Strategy, and Burnout Management for Georgia Tech's OMSCS".
>
> * This knowledge is incredibly difficult for prospective and current students to track down because official Georgia Tech pages only provide high-level academic requirements, whereas the real strategies for
    > survival—such as tracking historical class workloads, understanding pairing combinations to prevent burnout while working full-time, and decoding the strict foundational course requirements—are buried across
    > thousands of scattered forum reviews and multi-year Reddit threads.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | OMSHub Data Archive | Raw static catalog, tracking metadata, historical workload hours, and program constraints. | `https://github.com/omshub/data/tree/main/static` |
| 2 | Reddit Thread: Foundational Requirement | Student thread clarifying the reality of first-year rules and leniency regarding the "2 Bs in 12 months" policy. | `https://www.reddit.com/r/OMSCS/comments/1fskt68/foundational_course_requirement/` |
| 3 | Unofficial Orientation Guide FAQ | The official r/OMSCS Wiki serving as a hub for student-curated advice, track preparation, and administrative hacks. | `https://www.reddit.com/r/OMSCS/wiki/index/` |
| 4 | Reddit Thread: Comprehensive Data Review | Deep-dive individual retrospective review tracking a massive amount of personal data, metrics, and course thoughts. | `https://www.reddit.com/r/OMSCS/comments/12nh421/my_waytoomuch_data_omscs_review/` |
| 5 | Reddit Thread: 10-Class Journey Trip | A complete student retrospective reflecting on their path through all 10 courses to graduate the program. | `https://www.reddit.com/r/OMSCS/comments/12k57x1/finished_my_10th_class_my_trip_through_omscs/` |
| 6 | Reddit Thread: Computing Systems Track Review | Graduate review evaluating specific course selections and project difficulties within the Core Systems track. | `https://www.reddit.com/r/OMSCS/comments/12zn0ha/yet_another_omscs_review_computing_systems_track/` |
| 7 | Reddit Thread: Incompatible Class Pairings | Classic community advice thread mapping out which heavy-workload courses should never be paired together. | `https://www.reddit.com/r/OMSCS/comments/3qyup9/classes_not_to_take_together_and_classes_that_are/` |
| 8 | Reddit Comment: Pairing Deep-Dive Context | A high-value specific comment nested within course selection threads providing actionable pairing frameworks. | `https://www.reddit.com/r/OMSCS/comments/3rghng/comment/cwo0wqu/` |
| 9 | Reddit Megathread: Admissions Results & Chances | Crowdsourced repository of real applicant stats (GPA, background, prerequisites) and their acceptance outcomes. | `https://www.reddit.com/r/OMSCS/comments/1pyef6c/admissions_megathread_results_chances_and/` |
| 10 | Reddit Megathread: Course Specs & Capacity Logistics | Comprehensive thread tracking course selection strategies, registration dynamics, and capacity limitations. | `https://www.reddit.com/r/OMSCS/comments/1pyef5z/course_specs_megathread_selection_choices/` |
| 11 | Reddit Thread: 2025 Difficulty Rankings | Quantitative community leaderboard ranking all program courses by difficulty and weekly hours. | `https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/` |
| 12 | GT Computing Systems Spec | Official academic checklist tracking foundational choices and electives for the Core Systems specialization. | `https://omscs.gatech.edu/specialization-computing-systems` |
| 13 | GT Machine Learning Spec | Official curriculum, core courses, and elective options for the popular Machine Learning specialization. | `https://omscs.gatech.edu/specialization-machine-learning` |
| 14 | GT Artificial Intelligence Spec | Official requirements for the AI track (formerly known as Interactive Intelligence). | `https://omscs.gatech.edu/specialization-artificial-intelligence-formerly-interactive-intelligence` |
| 15 | GT Computational Perception & Robotics Spec | Official curriculum mapping for the intersection of computer vision, robotics, and physical systems. | `https://omscs.gatech.edu/specialization-computational-perception-and-robotics` |
| 16 | GT Computer Graphics Spec | Official academic guidelines and prerequisite tracks for the Computer Graphics specialization. | `https://omscs.gatech.edu/specialization-computer-graphics` |
| 17 | GT Human-Computer Interaction Spec | Official tracking sheet detailing requirements for interface design, evaluation, and user experience courses. | `https://omscs.gatech.edu/specialization-human-computer-interaction` |
| 18 | GT Research Opportunities Portal | Official institutional framework explaining how online students can pursue formal research (CS 6999). | `https://omscs.gatech.edu/research-opportunities` |
| 19 | GT Preparing Yourself for OMSCS | Official self-assessment page recommending specific mathematical foundations and programming competencies. | `https://omscs.gatech.edu/preparing-yourself-omscs` |
| 20 | GT Prospective Student FAQs | Official baseline information covering technical setup requirements, degree legitimacy, and proctoring. | `https://omscs.gatech.edu/prospective-student-faqs` |
| 21 | Academic Standing Regulations | Georgia Tech Registrar policy text (Rule 6) detailing rules on academic standing and transcript marks. | `https://catalog.gatech.edu/rules/6/` |
| 22 | GT Admission Criteria | Official baseline documentation for GPA minimums, academic background requirements, and documentation rules. | `https://omscs.gatech.edu/admission-criteria` |
| 23 | GT Application Deadlines & Guidelines | Official calendar timelines, letter of recommendation instructions, and portfolio requirements. | `https://omscs.gatech.edu/deadlines-decisions-requirements-and-guidelines` |
| 24 | GT Overall Degree Requirements | Institutional checklist for graduation: 30 credit hours, GPA floors, and core vs. elective splits. | `https://omscs.gatech.edu/degree-requirements` |
| 25 | GT Current Course Catalog | Official active inventory of courses currently being offered to online students in the active semester. | `https://omscs.gatech.edu/current-courses` |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

Summary of approach (from `planning.md` / `ingest.py`):
- Chunk size: ~300 tokens (the current implementation approximates tokens as words)
- Overlap: ~50 tokens
- Rules used by the ingester:
    - If a file contains dashed-line separators (3+ hyphens), split at those markers and emit each section as an atomic chunk.
    - If JSON: emit one chunk per top-level key (object) or per list element (if the file is a list).
    - Otherwise use recursive splitting on separators ["\n\n", "\n", ". ", " "] until pieces fit the chunk size, falling back to word-windowing with overlap.

Why these choices: preserves thread/post boundaries and structured JSON entries while keeping chunk sizes small enough for embeddings and LLM prompts. For production use, replace word-approximation with token-aware splitting (e.g., `tiktoken`).

Final chunk count: stored in `output/chunks.json` (open it after running `python ingest.py`).

## Embedding Model & Retrieval

- Embedding model used: `sentence-transformers` all-MiniLM-L6-v2 (local, fast)
- Retrieval top-k: 4 chunks per query (good balance of context vs token budget)

Production tradeoffs if cost weren't a constraint:
- Use larger embedding models (e.g., OpenAI text-embedding-3-large) for longer context windows and better semantic matching.
- Consider hybrid retrieval (BM25 lexical + dense embeddings + reranker) for speed and accuracy.
- Consider fine-tuning or domain-adapting embeddings to better handle OMSCS acronyms and slang.

---

## Grounded Generation (how we prevent hallucination)

This project enforces grounding using four complementary layers (see `GENERATION_GUIDE.md` and `query.py`):

1. System prompt (CRITICAL instruction): passed to the LLM to *require* the model to answer ONLY from the provided documents and to refuse when documents lack enough information. Example (stored in `query.py`):
"CRITICAL GROUNDING RULE: You must answer ONLY using the information provided in the documents below. If the documents do NOT contain enough information to answer the question, you MUST respond with:\n\"I don't have enough information on that topic in the available documents.\""
2. User prompt/context: the retrieved chunks are concatenated into a clearly labeled context block that the model must use.
3. Temperature control: `temperature=0.4` (low randomness to reduce creativity/hallucination).
4. Programmatic source attribution: sources are extracted from chunk metadata (the `source` field added during ingestion) — NOT parsed from LLM text. This guarantees the listed sources are the actual files used for retrieval.
Important parameters: `k=4` retrieved chunks, `temperature=0.4`. If no relevant chunks are found the engine returns the explicit refusal text immediately (no LLM call).

---

## Evaluation Summary

Run the test suite `python end_to_end_test.py` which runs several checks. Summary of the canonical 5 evaluation queries (from `planning.md`) and observed behavior:

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Preparatory courses for non-traditional applicants | List of CS foundational courses and the committee's preference for formal, for-credit evidence | Grounded in `documents/wikis/prospective-faqs` and admissions threads (sources cited). | Relevant | Accurate |
| 2 | Consequences of a low grade in foundational courses | Description of the 1-year rule and restrictions | Grounded in official policy docs from `documents/wikis` or cleaned policy threads. | Relevant | Accurate |
| 3 | Course pairings for GIOS (Operating Systems) while working full-time | Advice to pair GIOS with lower-workload electives | Grounded in student reviews (e.g., `course_difficulties.json.md`). | Relevant | Accurate / Good |
| 4 | Summer semester intensity vs Fall/Spring | Summer is shorter and more intense (e.g., 10–13 weeks vs ~15 weeks) | Grounded; test asserts the response mentions summer and weeks. | Relevant | Accurate |
| 5 | Differences between ML vs Computing Systems workload/style | ML is more theoretical/report-centric; Systems focuses on low-level, graded projects | Grounded across multiple documents. | Relevant | Accurate |

The included `end_to_end_test.py` asserts these behaviors and validates that the system returns explicit refusal for out-of-domain queries (e.g., "What is the salary for a ML engineer at Google?").

---

## Failure Case Analysis (example)

- Question that failed (typical failure mode): a reply-only comment saying "30 hours a week" was split away from its parent post and the chunk lacked context: the retrieval returned the isolated comment and the generator couldn't tie it to which course it referred to.
- What the system returned: a vague statement about high workload without specifying the course.
- Root cause: chunking split reply from parent (ingestion stage), leaving the chunk without anchoring metadata.
- Fix: during ingestion append thread title or parent post metadata to each child comment, or increase the chunk size for forum posts so replies and parent are kept together.

---

## Spec Reflection
- One way the spec helped: `planning.md` forced exact design decisions (chunk size, overlap, retrieval k=4, embedding choice) which made implementation deterministic and easier to test.
- One divergence: token accounting used a word-approximation rather than `tiktoken` tokenization (chosen for simplicity). For production I'd switch to a token-aware splitter to guarantee the prompt fits into model context windows.

---

## AI Usage (two concrete instances)

Instance 1: Building My Ingest Pipeline
- The Input: I handed the AI my chunking strategy from planning.md along with a few cleaned-up markdown files to use as a baseline.
- The AI's Output: It spit out a working draft of ingest.py that handled recursive text splitting, flagged dashed-line separators, and included special-case logic for JSON files.
- My Refinements: I stepped in to tune the chunk size down to roughly 300 tokens (using a word-count approximation), bumped the overlap to 50, and injected custom metadata fields to track source, chunk_id, and word_count.

Instance 2: My RAG Prompting & Generation
- The Input: I fed the AI my retrieval approach blueprint, the exact refusal phrasing I want to enforce, and my test queries.
- The AI's Output: It generated the first version of query.py, which laid out the core system prompt and structured the user message format.
- My Refinements: I hardened the refusal logic to make it airtight, added code to programmatically pull the metadata.source from retrieved chunks, and forced an early return to stop the LLM from hallucinating if the vector search comes up completely empty.
---

## How to run (quickstart)

1) Create a virtualenv and install requirements:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Ingest and build the vector store (if you change or add documents):
```bash
python ingest.py
python -c "from vector_store import VectorStore; VectorStore().build(force=True)"
```

3) Run end-to-end tests:
```bash
python end_to_end_test.py
```

4) Launch the web UI (Gradio):
```bash
python app.py
# Open http://localhost:7860
```

Environment notes: set `GROQ_API_KEY` in your environment if you want to use Groq LLM as configured in `query.py`.

---

## Files you will see in this repo (what they are and whether you need them)

- `ingest.py` — document ingestion & chunking. REQUIRED to rebuild the corpus when you add or change documents.
- `vector_store.py` — embedding and ChromaDB wrapper. REQUIRED for retrieval and experiments.
- `query.py` — grounded generation engine + LLM interface + programmatic source extraction. REQUIRED to answer queries.
- `app.py` — Gradio UI around `query.py`. OPTIONAL for CLI-only use but recommended for demos.
- `end_to_end_test.py` — runnable tests that validate grounding & retrieval. STRONGLY RECOMMENDED to run before submission.
- `retrieval_log.json` — audit trail of previous queries (auto-generated). KEEP for reproducibility; can be removed if you want to reset logs.
- `documents/` — source documents (wikis + cleaned reviews). REQUIRED input data.
- `output/chunks.json` — ingestion output (chunks). Keep if you want to avoid re-running ingest; safe to delete and re-generate.
- `chromadb/` — local ChromaDB persistence (vectors). Keep for fast local runs; you can delete to rebuild.
- `requirements.txt` — Python dependencies. REQUIRED to reproduce environment.
- `GENERATION_GUIDE.md`, `GROUNDING_QUICK_REFERENCE.md`, `IMPLEMENTATION_COMPLETE.md`, `planning.md` — documentation. OPTIONAL to keep, but valuable; include them in your submission.
- `cleanup_util.py` — helper utilities for cleaning/remapping data. OPTIONAL but useful during ingestion.

Files to remove if repo needs to be shrunk: local DB files in `chromadb/` (these can be regenerated), `output/` if `ingest.py` can be re-ran, and any cached `__pycache__` directories. Keep source code and `documents/`.

---

