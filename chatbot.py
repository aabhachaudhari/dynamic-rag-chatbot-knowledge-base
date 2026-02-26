# chatbot.py
# Ask questions — answers come ONLY from your local files

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# ── CONFIG ──────────────────────────────────────────────────────────────────
DB_FOLDER        = "vector_db"
MODEL_NAME       = "all-MiniLM-L6-v2"
TOP_K            = 3        # how many chunks to retrieve
SIMILARITY_CUTOFF = 0.45    # below this score → "not in my sources"
# ────────────────────────────────────────────────────────────────────────────


def load_db():
    """Load the FAISS index and chunk metadata from disk."""
    index_path  = os.path.join(DB_FOLDER, "index.faiss")
    chunks_path = os.path.join(DB_FOLDER, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        print("\n  [✗] Vector DB not found.")
        print("  Please run:  python ingest.py   first.\n")
        exit(1)

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def search(query, index, chunks, model, top_k=TOP_K):
    """Embed the query and search the FAISS index."""
    query_vec = model.encode([query], convert_to_numpy=True)

    # Normalise
    query_vec = query_vec / np.linalg.norm(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "text"  : chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "score" : float(score)
        })

    return results


def answer_question(query, index, chunks, model):
    """Search and format the answer."""
    results = search(query, index, chunks, model)

    # Filter by similarity cutoff
    good_results = [r for r in results if r["score"] >= SIMILARITY_CUTOFF]

    if not good_results:
        return "I don't know (not in my sources).", []

    return good_results[0]["text"], good_results


def print_answer(query, index, chunks, model):
    """Print a nicely formatted answer to the terminal."""
    print("\n" + "─" * 55)
    print(f"  Q: {query}")
    print("─" * 55)

    answer, results = answer_question(query, index, chunks, model)

    if not results:
        print(f"  A: {answer}")
    else:
        print(f"  A: {answer}")
        print(f"\n  📄 Source : {results[0]['source']}")
        print(f"  📊 Confidence : {results[0]['score']:.2f}")

        # Show other relevant chunks if found
        if len(results) > 1:
            print("\n  Also found in:")
            for r in results[1:]:
                print(f"    • [{r['source']}] (score: {r['score']:.2f})")
                print(f"      {r['text'][:120]}...")

    print("─" * 55)


def main():
    print("=" * 55)
    print("     DYNAMIC KNOWLEDGE BASE CHATBOT")
    print("     (answers only from your local files)")
    print("=" * 55)

    print("\nLoading model and database...")
    model  = SentenceTransformer(MODEL_NAME)
    index, chunks = load_db()
    print(f"  [✓] Ready! ({len(chunks)} chunks loaded)\n")
    print("  Type your question and press Enter.")
    print("  Type  'quit'  or  'exit'  to stop.\n")

    while True:
        try:
            query = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye!")
            break

        print_answer(query, index, chunks, model)


if __name__ == "__main__":
    main()