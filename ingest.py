"""ingest.py

Create chunks from documents according to the project's planning.md:
 - Recursive character splitting using separators ["\n\n", "\n", ". ", " "]
 - Chunk size: 300 tokens (approximated as 300 words)
 - Overlap: 50 tokens (approximated as 50 words)

The script scans `documents/wikis/` and `documents/reviews_cleaned/`, produces
a JSON file with chunk text and metadata, and prints 5 representative chunks.
"""
from pathlib import Path
import json
import argparse
import math
from typing import List
import re


CHUNK_SIZE = 300  # approximated as words
CHUNK_OVERLAP = 50  # approximated as words
SEPARATORS = ["\n\n", "\n", ". ", " "]


def word_count(text: str) -> int:
    return len(text.strip().split()) if text and text.strip() else 0


def split_by_words_with_overlap(text: str, chunk_size: int, overlap: int) -> List[str]:
    words = text.strip().split()
    if not words:
        return []
    step = max(chunk_size - overlap, 1)
    chunks = []
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if i + chunk_size >= len(words):
            break
    return chunks


def split_recursive(text: str, separators: List[str], chunk_size: int) -> List[str]:
    """Recursively split `text` on the provided separators until pieces are
    smaller than `chunk_size` (in words). Falls back to word-based chunking
    with overlap when no separator breaks the text further.
    """
    text = text.strip()
    if not text:
        return []
    if word_count(text) <= chunk_size:
        return [text]

    for sep in separators:
        parts = [p.strip() for p in text.split(sep) if p.strip()]
        if len(parts) > 1:
            chunks = []
            for part in parts:
                if word_count(part) <= chunk_size:
                    chunks.append(part)
                else:
                    # recursively split this part further (same separators)
                    chunks.extend(split_recursive(part, separators, chunk_size))
            return chunks

    # No separator produced smaller parts; split by words with overlap
    return split_by_words_with_overlap(text, chunk_size, CHUNK_OVERLAP)


def ingest_documents(root: Path) -> List[dict]:
    """Load files under `root/documents/wikis` and `root/documents/reviews_cleaned`
    and produce a list of chunks with metadata.
    """
    docs_dir = root / "documents"
    sources = [docs_dir / "wikis", docs_dir / "reviews_cleaned"]
    all_chunks = []

    for src in sources:
        if not src.exists():
            continue
        for path in sorted(src.rglob("*")):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                # try with latin-1 fallback
                try:
                    text = path.read_text(encoding="latin-1")
                except Exception:
                    # skip unreadable files
                    continue

            # normalize whitespace
            text = text.replace("\r", "\n").strip()
            if not text:
                continue

            # Pre-split on dashed-line separators (lines containing 3+ hyphens).
            # e.g., ----------------------------------------
            dash_pattern = re.compile(r"\n\s*-{3,}\s*\n")
            if dash_pattern.search(text):
                parts = [p.strip() for p in dash_pattern.split(text) if p.strip()]
                for sec_idx, part in enumerate(parts):
                    chunk_text = part
                    all_chunks.append({
                        "source": str(path.relative_to(root)),
                        "source_abs": str(path.resolve()),
                        "chunk_id": f"{path.stem}--section{sec_idx}",
                        "text": chunk_text,
                        "word_count": word_count(chunk_text),
                    })
                continue

            # Special-case JSON files: emit one chunk per top-level dict entry
            # (e.g., course-stats.json -> one chunk per course) or per list
            if path.suffix.lower() == ".json":
                try:
                    parsed = json.loads(text)
                except Exception:
                    parsed = None

                if isinstance(parsed, dict):
                    for key, val in parsed.items():
                        chunk_text = json.dumps({key: val}, ensure_ascii=False, indent=2)
                        all_chunks.append({
                            "source": str(path.relative_to(root)),
                            "source_abs": str(path.resolve()),
                            "chunk_id": f"{path.stem}--{key}",
                            "text": chunk_text,
                            "word_count": word_count(chunk_text),
                        })
                    continue

                if isinstance(parsed, list):
                    for i_elem, elem in enumerate(parsed):
                        chunk_text = json.dumps(elem, ensure_ascii=False, indent=2)
                        all_chunks.append({
                            "source": str(path.relative_to(root)),
                            "source_abs": str(path.resolve()),
                            "chunk_id": f"{path.stem}--{i_elem}",
                            "text": chunk_text,
                            "word_count": word_count(chunk_text),
                        })
                    continue

            # Fallback: recursive splitting using separators and word-based overlap
            chunks = split_recursive(text, SEPARATORS, CHUNK_SIZE)
            # Attach metadata and sequential chunk id for traceability
            for i, c in enumerate(chunks):
                all_chunks.append({
                    "source": str(path.relative_to(root)),
                    "source_abs": str(path.resolve()),
                    "chunk_id": f"{path.stem}--{i}",
                    "text": c,
                    "word_count": word_count(c),
                })

    return all_chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="project root directory", default=".")
    parser.add_argument("--out", help="output JSON file", default="output/chunks.json")
    parser.add_argument("--preview", help="number of sample chunks to print", type=int, default=5)
    args = parser.parse_args()

    root = Path(args.root)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Ingesting documents under: {root / 'documents'}")
    chunks = ingest_documents(root)
    print(f"Produced {len(chunks)} chunks")

    # Save JSON
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # Print representative chunks
    n = min(args.preview, len(chunks))
    print(f"\nPrinting {n} representative chunks:\n")
    for i in range(n):
        item = chunks[i]
        print(f"--- Chunk {i+1}/{n} (source={item['source']}, words={item['word_count']}) ---")
        snippet = item['text']
        # print only first 400 chars of snippet for readability
        print(snippet[:400].replace('\n', ' '))
        print("\n")


if __name__ == "__main__":
    main()



