# ingest.py
# Run this ONCE to build your vector database from your files + URLs

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pypdf import PdfReader
from url_loader import fetch_url, load_urls_from_file

# ── CONFIG ───────────────────────────────────────────────────────────────────
TEXT_FILE  = "data/sample.txt"
URLS_FILE  = "data/urls.txt"
PDF_FOLDER = "sources"
DB_FOLDER  = "vector_db"
CHUNK_SIZE = 3
MODEL_NAME = "all-MiniLM-L6-v2"
# ─────────────────────────────────────────────────────────────────────────────


def read_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read(), os.path.basename(filepath)


def read_pdf_file(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text, os.path.basename(filepath)


def split_into_chunks(text, source_name, chunk_size=CHUNK_SIZE):
    sentences = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split(". ")
        for part in parts:
            part = part.strip()
            if len(part) > 20:
                sentences.append(part)

    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk_text = ". ".join(sentences[i : i + chunk_size])
        chunks.append({"text": chunk_text, "source": source_name})

    return chunks


def load_all_documents():
    all_chunks = []

    # 1. Load sample.txt
    if os.path.exists(TEXT_FILE):
        text, source = read_text_file(TEXT_FILE)
        chunks = split_into_chunks(text, source)
        all_chunks.extend(chunks)
        print(f"  [OK] Text file : {source}  ->  {len(chunks)} chunks")
    else:
        print(f"  [!] Not found  : {TEXT_FILE}")

    # 2. Load PDFs
    if os.path.exists(PDF_FOLDER):
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
        for pdf_file in pdf_files:
            path = os.path.join(PDF_FOLDER, pdf_file)
            text, source = read_pdf_file(path)
            chunks = split_into_chunks(text, source)
            all_chunks.extend(chunks)
            print(f"  [OK] PDF       : {source}  ->  {len(chunks)} chunks")

    # 3. Load URLs
    urls = load_urls_from_file(URLS_FILE)
    if urls:
        print(f"\n  Found {len(urls)} URLs in {URLS_FILE}. Fetching...\n")
        success = 0
        for url in urls:
            text, source = fetch_url(url)
            if text.strip():
                chunks = split_into_chunks(text, source)
                all_chunks.extend(chunks)
                print(f"  [OK] URL       : {source}  ->  {len(chunks)} chunks")
                success += 1
        print(f"\n  URLs loaded: {success}/{len(urls)} succeeded")
    else:
        print("  [i] No URLs to load")

    return all_chunks


def build_vector_db(chunks, model):
    print("\n  Generating embeddings...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index, embeddings


def save_db(index, chunks):
    os.makedirs(DB_FOLDER, exist_ok=True)
    faiss.write_index(index, os.path.join(DB_FOLDER, "index.faiss"))
    with open(os.path.join(DB_FOLDER, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
    print(f"\n  [OK] Vector DB saved to '{DB_FOLDER}/'")


def main():
    print("=" * 60)
    print("         KNOWLEDGE BASE INGESTOR  (with URLs)")
    print("=" * 60)

    print("\n[1] Loading all documents + URLs...")
    chunks = load_all_documents()

    if not chunks:
        print("\n  [FAIL] No content found. Check your files and URLs.")
        return

    print(f"\n  Total chunks ready for indexing: {len(chunks)}")

    print("\n[2] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print(f"  [OK] Model loaded : {MODEL_NAME}")

    print("\n[3] Building FAISS vector database...")
    index, _ = build_vector_db(chunks, model)

    print("\n[4] Saving to disk...")
    save_db(index, chunks)

    print("\n" + "=" * 60)
    print("  Done! Run: python chatbot.py")
    print("=" * 60)


if __name__ == "__main__":
    main()