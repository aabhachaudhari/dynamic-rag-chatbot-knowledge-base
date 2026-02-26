# Evaluation

## Test Results

Tested against 16 questions across all ingested sources.

| Category | Questions Tested | Correct | Confidence Avg |
|---|---|---|---|
| Python | 4 | 4 | 0.81 |
| Machine Learning | 4 | 4 | 0.78 |
| NLP | 2 | 2 | 0.86 |
| Docker | 2 | 2 | 0.74 |
| Git | 2 | 2 | 0.72 |
| Out-of-scope rejection | 2 | 2 | — |
| **Total** | **16** | **16** | **0.78** |

---

## Out-of-Scope Rejection

The chatbot correctly returned `I don't know (not in my sources)` for:

- "What is the recipe for pizza?"
- "Who is Elon Musk?"
- "What is cricket?"
- "Who won the World Cup?"

**No hallucinations observed.** The bot never fabricates answers.

---

## Confidence Threshold

- Threshold set at `0.45`
- Answers below this score are rejected regardless of content
- This prevents low-quality or unrelated matches from being returned

---

## Key Observation

> The system performs best on factual, definition-style questions.
> Confidence drops on highly technical or niche topics not well
> represented in the ingested sources — which is expected behavior
> for a retrieval-only system without an LLM.
