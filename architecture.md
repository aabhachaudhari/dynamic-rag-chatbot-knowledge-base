# Architecture

## How It Works — 3 Stages

### Stage 1 — Ingestion (`ingest.py`)
1. Reads content from `data/sample.txt`, PDFs in `sources/`, and URLs in `data/urls.txt`
2. Splits content into overlapping text chunks (3 sentences per chunk)
3. Passes each chunk through the `all-MiniLM-L6-v2` sentence transformer
4. Generates a 384-dimensional embedding vector for each chunk
5. Stores all vectors in a FAISS `IndexFlatIP` (cosine similarity index)
6. Saves the index and chunk metadata to `vector_db/`

### Stage 2 — Query (`chatbot.py`)
1. User types a question
2. Question is embedded using the same sentence transformer model
3. FAISS searches for the top 3 most similar chunks
4. If the best match score is below `0.45`, returns "I don't know"
5. Otherwise returns the best matching chunk + source name + confidence score

### Stage 3 — Caching (`url_loader.py`)
1. URLs are fetched once and saved as `.txt` files in `data/url_cache/`
2. On subsequent runs, cached files are used — no internet needed
3. Wikipedia pages use a dedicated parser that strips citations,
   footnotes, math formulas, and reference sections

---

## Folder Structure
```
knowledge_chatbot/
│
├── data/
│   ├── sample.txt          ← local knowledge file
│   ├── urls.txt            ← list of source URLs
│   └── url_cache/          ← auto-cached URL content
│
├── sources/                ← drop PDF files here
├── vector_db/              ← auto-generated FAISS index
│
├── ingest.py               ← builds the vector database
├── chatbot.py              ← question answering interface
└── url_loader.py           ← URL fetching and cleaning
```

---

## Embedding Model

- Model: `all-MiniLM-L6-v2` from `sentence-transformers`
- Vector size: 384 dimensions
- Similarity metric: Cosine similarity (via dot product on normalized vectors)
- Runs fully locally — no HuggingFace token required