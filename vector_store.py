"""
vector_store.py

Implements:
 - loading chunks produced by `ingest.py` (output/chunks.json)
 - embedding them with SentenceTransformer("all-MiniLM-L6-v2")
 - storing vectors + metadata in a local ChromaDB collection
 - a retrieve_docs(query, k=4) function that returns top-k chunks with scores

Run as a script to (re)create the collection and run a few example queries from planning.md.
"""
import json
import os
import sys
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    print("ERROR: sentence-transformers is required. See requirements.txt.\n", e)
    raise

try:
    import chromadb
    from chromadb.config import Settings
except Exception:
    # chromadb API surface changed over versions; we'll try to import the common surface and
    # fall back to a basic client() constructor if Settings is not available.
    import chromadb
    Settings = None


CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "output", "chunks.json")
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chromadb")
COLLECTION_NAME = "omscs_chunks"


def load_chunks(path: str) -> List[Dict[str, Any]]:
    """Load chunk objects produced by ingest.py. Expected format: list of dicts with
    keys like 'text', 'source', 'chunk_id', 'word_count', etc.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of chunks in {path}")
    return data


def _init_chroma_client(persist_dir: str = CHROMA_PERSIST_DIR):
    """Initialize a chromadb client with a persistent directory when possible.
    This handles different chromadb versions by trying Settings first.
    """
    try:
        if Settings is not None:
            client = chromadb.Client(Settings(persist_directory=persist_dir))
        else:
            client = chromadb.Client()
    except Exception:
        # Final fallback
        client = chromadb.Client()
    return client


def create_collection(client, name: str):
    """Create or get a collection named `name`.
    Uses get_or_create_collection when available; otherwise falls back to get/create.
    """
    try:
        collection = client.get_or_create_collection(name=name)
    except Exception:
        # Some versions use create_collection / get_collection
        try:
            collection = client.get_collection(name)
        except Exception:
            collection = client.create_collection(name)
    return collection


class VectorStore:
    def __init__(self, chunks_path: str = CHUNKS_PATH, persist_dir: str = CHROMA_PERSIST_DIR):
        self.chunks_path = chunks_path
        self.persist_dir = persist_dir
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = _init_chroma_client(persist_dir)
        self.collection = create_collection(self.client, COLLECTION_NAME)

    def build(self, force: bool = False, batch_size: int = 128):
        """Embed all chunks and add them to the ChromaDB collection.
        If force=True, the collection will be re-created (old vectors removed).
        """
        if force:
            # Try to delete and recreate the collection to ensure a fresh start
            try:
                self.client.delete_collection(name=COLLECTION_NAME)
            except Exception:
                pass
            self.collection = create_collection(self.client, COLLECTION_NAME)

        chunks = load_chunks(self.chunks_path)
        print(f"Loaded {len(chunks)} chunks from {self.chunks_path}")

        # Build lists for documents, metadatas, and ids
        ids = []
        documents = []
        metadatas = []

        for i, c in enumerate(chunks):
            cid = c.get("chunk_id") or f"chunk_{i}"
            ids.append(str(cid))
            documents.append(c.get("text", ""))
            # minimal metadata includes source and position
            metadatas.append({
                "source": c.get("source"),
                "source_abs": c.get("source_abs"),
                "chunk_id": cid,
                "word_count": c.get("word_count"),
            })

        # Compute embeddings in batches to avoid OOM
        print("Computing embeddings with all-MiniLM-L6-v2...")
        embeddings = self.model.encode(documents, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True)

        # Add to chroma collection. Most chroma versions accept ids, metadatas, documents, embeddings
        try:
            self.collection.add(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings.tolist())
        except Exception:
            # some chroma versions accept numpy arrays directly
            self.collection.add(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings)

        # Persist if supported
        try:
            self.client.persist()
        except Exception:
            # persist might not be implemented in some versions or when using ephemeral client
            pass

        print(f"Indexed {len(ids)} items into collection '{COLLECTION_NAME}'")

    def retrieve(self, query: str, k: int = 4):
        """Retrieve top-k chunks for `query`.
        Returns list of dicts: {id, document, metadata, distance}
        """
        q_emb = self.model.encode([query], convert_to_numpy=True)
        try:
            # chromadb expects include to be a subset of: documents, embeddings, metadatas, distances, uris, data
            results = self.collection.query(query_embeddings=q_emb, n_results=k, include=['metadatas', 'distances', 'documents'])
        except Exception:
            # fallback to text query API
            results = self.collection.query(query_texts=[query], n_results=k, include=['metadatas', 'distances', 'documents'])

        out = []
        ids = results.get('ids', [[]])[0]
        docs = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]

        for i in range(len(ids)):
            out.append({
                'id': ids[i],
                'document': docs[i],
                'metadata': metadatas[i],
                'distance': distances[i],
            })
        return out


def _run_examples():
    store = VectorStore()
    # If collection looks empty, build index
    # Heuristic: try a small query and see if we get results
    sample = store.retrieve("operating systems workload", k=1)
    if not sample:
        print("No results found in collection; building index now (this may take a few minutes)...")
        store.build(force=True)

    test_queries = [
        # From planning.md evaluation plan
        "What preparatory computer science courses should a non-traditional applicant take to maximize their chances of admission into OMSCS?",
        "What are the best low-workload courses to pair with Graduate Introduction to Operating Systems (CS 6200) for someone working full-time?",
        "How does the intensity of taking a course during the shortened summer semester compare to a standard Fall or Spring semester?",
    ]

    for q in test_queries:
        print("\n=== QUERY ===")
        print(q)
        results = store.retrieve(q, k=4)
        if not results:
            print("No results returned.")
            continue
        for r in results:
            print(f"\n- id: {r['id']}  distance: {r['distance']}")
            src = r['metadata'].get('source') if r.get('metadata') else None
            print(f"  source: {src}")
            snippet = r['document'][:400].replace('\n', ' ')
            print(f"  snippet: {snippet}...")


if __name__ == '__main__':
    # Run the example retrievals. This script is safe to run repeatedly; set force=True in build() to reindex.
    _run_examples()


