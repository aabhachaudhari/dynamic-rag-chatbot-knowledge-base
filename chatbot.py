from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)

print("🤖 Chatbot ready! Type 'exit' to quit.")

while True:
    q = input("You: ")
    if q.lower() == "exit":
        break

    results = db.similarity_search(q, k=1)
    if results:
        doc = results[0]
        print("Bot:", doc.page_content)
        print("Source:", doc.metadata.get("source", "unknown"))
    else:
        print("Bot: I couldn't find anything relevant.")

    # Show last updated time (if available)
try:
    with open("last_updated.txt", "r", encoding="utf-8") as f:
        last_updated = f.read().strip()
    print(f"🕒 Last updated: {last_updated}\n")
except FileNotFoundError:
    print("🕒 Last updated: not available yet\n")