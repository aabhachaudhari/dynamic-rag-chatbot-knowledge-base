from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup

# 1. Load existing vector DB
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)

# 2. Source URL 
URL = "https://huggingface.co/docs"

# 3. Fetch webpage content
response = requests.get(URL, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")

# Extract visible text
text = soup.get_text(separator=" ", strip=True)

# 4. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(text)

# 5. Add to existing DB
db.add_texts(chunks)
db.save_local("vector_db")

from datetime import datetime

with open("last_updated.txt", "w", encoding="utf-8") as f:
    f.write(datetime.now().strftime("%d %b %Y, %H:%M"))

print("🕒 Last updated timestamp saved.")

print("🔁 Knowledge base updated from HuggingFace docs!")EXIT