# Usage

## Starting the Chatbot
```bash
python chatbot.py
```

Type any question and press Enter. Type `quit` to exit.

---

## Example Session
```
You: What is Python?
─────────────────────────────────────────────
Q: What is Python?
A: Python is a high-level, general-purpose programming language.
   Its design philosophy emphasizes code readability.

📄 Source : en.wikipedia.org
📊 Confidence : 0.84
─────────────────────────────────────────────

You: What is the recipe for pizza?
─────────────────────────────────────────────
Q: What is the recipe for pizza?
A: I don't know (not in my sources).
─────────────────────────────────────────────
```

---

## Adding New Sources

| Source type | What to do |
|---|---|
| Text file | Edit `data/sample.txt` |
| PDF | Drop file into `sources/` folder |
| Website | Add URL to `data/urls.txt` |

Then rebuild: `python ingest.py`

---

## Demo Questions
```
What is Python?
Who created Python?
What is machine learning?
What is supervised learning?
What is natural language processing?
What is tokenization?
What is Docker?
What is a Docker container?
What is Git?
What is version control?
```