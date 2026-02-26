# Limitations

## Current Limitations

### 1. No language understanding
The chatbot uses **semantic similarity**, not language understanding.
It retrieves the closest matching chunk — it does not reason, summarize,
or synthesize answers across multiple sources.

### 2. Answer quality depends on source quality
If a webpage has noisy content (ads, menus, footers), the ingested
chunks may be irrelevant. Wikipedia works best due to its clean structure.

### 3. No conversation memory
Each question is answered independently. The chatbot has no memory
of previous questions in the same session.

### 4. Chunk boundary limitations
Long answers may be cut off at chunk boundaries. If a concept spans
multiple paragraphs, only one chunk is returned as the answer.

### 5. Static knowledge base
The vector database must be manually rebuilt after adding new sources.
There is no real-time or automatic update mechanism.

### 6. English only
The embedding model (`all-MiniLM-L6-v2`) is optimized for English.
Performance on other languages is not guaranteed.

---

## Planned Improvements

- [ ] Add multi-turn conversation memory
- [ ] Support automatic re-ingestion when sources change
- [ ] Experiment with larger embedding models for better accuracy
- [ ] Add a simple web UI using Streamlit
- [ ] Support more file types (`.docx`, `.csv`)
