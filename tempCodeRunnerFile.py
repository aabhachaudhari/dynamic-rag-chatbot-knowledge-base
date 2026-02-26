from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load data
loader = TextLoader("data/sample.txt")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_documents(docs)

# 3. Convert text to embeddings (numbers)
embeddings = HuggingFaceEmbeddings()

# 4. Store in vector database
db = FAISS.from_documents(chunks, embeddings)
db.save_local("vector_db")

print("✅ Knowledge base created successfully!")