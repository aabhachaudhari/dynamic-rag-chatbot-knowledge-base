# Dynamic Knowledge Base Chatbot (RAG)

This project implements a chatbot with a dynamically expanding knowledge base using embeddings and a vector database.  
New information can be added over time and the chatbot updates its responses automatically.

## Problem
Normal chatbots cannot answer questions about newly added information.

## Solution
I built a Retrieval-Augmented Generation (RAG) system where:
- Text is converted into embeddings  
- Stored in a vector database  
- Relevant information is retrieved using semantic search  
- The knowledge base can be updated without retraining the model  

## Tech Stack
- Python  
- LangChain  
- FAISS  
- HuggingFace Sentence Transformers  

## How to Run
1. Create the knowledge base:
python ingest.py
2. Update the knowledge base:
python update.py
3. Start the chatbot:
python chatbot.py

## Result
The chatbot answers questions based on newly added information.

## 🔁 Live Update Support
The knowledge base can be updated from web sources using `update.py`, and changes are reflected without rebuilding the entire vector database.