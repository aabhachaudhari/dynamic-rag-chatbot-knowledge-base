# Setup Guide

## Requirements

- Python 3.10 or higher
- Windows / Mac / Linux
- VS Code (recommended)

---

## Installation

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/dynamic-chatbot-knowledge-base.git
cd dynamic-chatbot-knowledge-base
```

### Step 2 — Install dependencies
```bash
pip install sentence-transformers faiss-cpu pypdf numpy requests beautifulsoup4 lxml
```

### Step 3 — Add your sources
- Edit `data/sample.txt` with your own knowledge
- Add PDF files to `sources/`
- Add URLs to `data/urls.txt` (one per line)

### Step 4 — Build the vector database
```bash
python ingest.py
```

### Step 5 — Start chatting
```bash
python chatbot.py
```

---

## Current Sources (`data/urls.txt`)
```
https://en.wikipedia.org/wiki/Python_(programming_language)
https://en.wikipedia.org/wiki/Machine_learning
https://en.wikipedia.org/wiki/Natural_language_processing
https://en.wikipedia.org/wiki/Docker_(software)
https://en.wikipedia.org/wiki/Git
```

---

## Rebuilding After Adding New Sources

Whenever you add new files or URLs, rebuild the database:
```bash
rmdir /s /q data\url_cache    # Windows
python ingest.py
```
