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

Run the test suite `python end_to_end_test.py` which runs several checks. 
Summary of the canonical 5 evaluation queries (from `planning.md`) and observed behavior:

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What preparatory computer science courses should a non-traditional applicant take to maximize their chances of admission into OMSCS? | The admissions committee looks for documented, for-credit academic transcripts showing a grade of B or better in fundamental programming, object-oriented design, data structures, and algorithms. High-quality regional options frequently cited by the community include specific sequence classes from Oakton Community College or Foothill College. Standard MOOC certificates and bootcamps are rarely considered rigorous enough on their own. | The system accurately identified that non-traditional applicants should focus on documented, for-credit courses in fundamental programming, object-oriented design, data structures, and algorithms, citing specific institutions like Oakton Community College or Foothill College, and noted that MOOCs or bootcamps are generally insufficient. | Relevant | Accurate |
| 2 | What are the exact consequences if a student gets a C or below in a foundational course during their first three semesters? | Under official academic policy, a student has exactly one calendar year (3 consecutive semesters) from matriculation to complete the foundational requirement by passing two foundational courses with a B or better. Earning a C or withdrawing (W) does not trigger immediate dismissal, but it consumes one of those semesters. If the requirement is not met by the end of the first year, the student is restricted to taking *only* foundational courses until it is fulfilled. | The system correctly explained the official academic policy regarding foundational courses, including the one-year (three-semester) deadline, the impact of a C grade or withdrawal, and the restriction to foundational courses if the requirement isn't met. | Relevant | Accurate |
| 3 | Based on student consensus, what are the best "low-workload" courses to pair with Graduate Introduction to Operating Systems (CS 6200) for someone working full-time? | Historical student review trends on OMSCentral highlight that CS 6200 (GIOS) requires a demanding 15–20 hours per week due to complex C/C++ projects. To maintain sanity while working a full-time software engineering job, students recommend pairing it with lower-intensity electives like CS 6750 (Human-Computer Interaction) or CS 6310 (Software Architecture and Design), which typically average under 10–12 hours per week. | The system identified GIOS as a high-workload course (15-20 hours/week) and suggested pairing it with lower-intensity electives such as CS 6750 (Human-Computer Interaction) or CS 6310 (Software Architecture and Design), which average 10-12 hours/week, based on student reviews. | Relevant | Accurate |
| 4 | How does the intensity of taking a course during the shortened summer semester compare to a standard Fall or Spring semester? | The summer term condenses identical course material, projects, and exams from a standard 16-week timeline down into an intense, accelerated 11-week schedule. Students warn that weekly time commitments effectively increase by roughly 30-40%. Consequently, academic policy restricts enrollment to a maximum of one course during summer terms to prevent widespread burnout. | The system explained that summer semesters condense 16 weeks of material into 11 weeks, increasing weekly time commitments by 30-40%, and noted the policy restricting enrollment to one course to prevent burnout. | Relevant | Accurate |
| 5 | What are the key differences in formatting, workload, and coding assignments between the Machine Learning course and the Computing Systems track core requirements? | Machine Learning (CS 7641) is open-ended, heavily theoretical, and centers on writing extensive 10-15 page analysis reports evaluating model behaviors across various datasets rather than optimizing code performance. In contrast, Computing Systems core classes (like Advanced Operating Systems or GIOS) are structured around strict, deterministic automated grading setups (Gradescope/C-Test suites) testing robust low-level systems programming and memory management. | The system differentiated Machine Learning (CS 7641) as theoretical and report-centric, focusing on model analysis, from Computing Systems core courses (like GIOS) which are structured around strict, automated grading of low-level systems programming and memory management. | Relevant | Accurate |

The included `end_to_end_test.py` asserts these behaviors and validates that the system returns explicit refusal for out-of-domain queries (e.g., "What is the salary for a ML engineer at Google?").

---

## Failure Case Analysis (example)

- Question that failed (typical failure mode): A user asks about the workload for a specific course, say "CS 6200".
- What the system returned: A vague statement about high workload without specifying the course, or it might return information about a different course with a similar workload.
- Root cause: The "Lost Context in Reddit Replies" challenge identified in `planning.md`. A specific comment like "Don't do it, it's a massive trap. The workload is easily 30 hours a week and the exams are brutal." was split away from its parent post during the **chunking stage**. This left the chunk without anchoring metadata (e.g., the course name it referred to). Consequently, the **retrieval stage** might return this isolated comment, but the **generation stage** cannot accurately attribute the workload to "CS 6200" because the necessary context was lost. The embedding model might find the "30 hours a week" relevant to "workload", but without the course identifier in the same chunk or its metadata, the LLM cannot form a specific answer.
- Fix: During ingestion, a preprocessing step could append the thread title or parent topic to each child comment. Alternatively, increasing the chunk size for forum posts could keep replies and their parent context together, though this might lead to larger, less precise chunks for other document types.

- Question that failed: "What is GIOS?"
- What the system returned: "I don't have enough information on that topic in the available documents." (or a similar refusal, or a generic statement about "a course" without specific details).
- Root cause: The "Unofficial Acronym Soup" challenge identified in `planning.md`. While `documents/wikis/courses.json` contains "GIOS" as an `alias` for "CS-6200 Introduction to Operating Systems", the current **ingestion and embedding pipeline** does not explicitly leverage these aliases to enrich the chunk content. When the `courses.json` file is chunked, the text embedded for CS-6200 primarily contains its full name and description, but not necessarily the acronym "GIOS" within the main text body of the chunk itself. Therefore, when a query like "What is GIOS?" is embedded, the semantic similarity to the chunks containing the full course name is insufficient for effective retrieval, leading to a lack of relevant context for the **generation stage**.
- Fix: Modify the `ingest.py` script to explicitly incorporate aliases into the chunk's content or metadata. For example, when processing `courses.json`, the chunk text for CS-6200 could be augmented to include its aliases: "CS-6200 Introduction to Operating Systems (GIOS, IOS, OS)...". This ensures that the embedded representation of the chunk is semantically closer to queries using these common acronyms.

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

---