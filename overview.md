# Dynamic Knowledge Base Chatbot

A locally-running chatbot that answers questions **only from your own sources** — 
no OpenAI, no API keys, no internet required at runtime.

Built with Python using semantic search and a FAISS vector database.

---

## What It Does

- Ingests knowledge from local text files, PDFs, and URLs
- Converts content into vector embeddings using a local sentence transformer model
- Stores embeddings in a FAISS vector database for fast similarity search
- Answers questions based only on ingested sources
- Shows the **source file or URL** and a **confidence score** with every answer
- Replies with `I don't know (not in my sources)` when the answer isn't found

---

## Why I Built This

Most chatbots rely on large cloud-based LLMs and require API keys.
This project explores how to build a fully **offline, source-controlled** question 
answering system using only open-source tools — making it transparent, 
auditable, and easy to extend.

---

## Tech Stack

| Component | Tool |
|---|---|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector DB | `FAISS` (Facebook AI Research) |
| PDF parsing | `pypdf` |
| URL scraping | `requests` + `BeautifulSoup4` |
| Language | Python 3.10+ |