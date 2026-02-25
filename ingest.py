from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

print("📄 Loading data...")
loader = TextLoader("data/sample.txt", encoding="utf-8")
docs = loader.load()

print("✂ Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

print("🔢 Creating embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("💾 Creating vector DB...")
db = FAISS.from_documents(chunks, embeddings)
db.save_local("vector_db")

print("✅ vector_db created successfully!")
print("📁 Current files:", os.listdir("."))