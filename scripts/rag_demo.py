import os
import sys
from dotenv import load_dotenv

# Add backend to sys path to ensure we can import if needed, though mostly using installed packages
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../backend/.env'))

def main():
    print("--- LicitatieAI RAG Demo ---")

    # 1. Load Data
    file_path = os.path.join(os.path.dirname(__file__), '../data/legislation/sample_law.txt')
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print(f"Loading law text from: {file_path}")
    loader = TextLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s).")

    # 2. Split Data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # 3. Initialize Embeddings
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and not api_key.startswith("your_"):
        print("Using OpenAI Embeddings.")
        embeddings = OpenAIEmbeddings()
    else:
        print("WARNING: OPENAI_API_KEY not found or invalid. Using FakeEmbeddings (Random results).")
        # vector size 1536 matches OpenAI default
        embeddings = FakeEmbeddings(size=1536)

    # 4. Create Vector Store (Chroma)
    print("Creating Vector Store...")
    # We use a temporary in-memory store for the demo
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)

    # 5. Query
    query = "Care sunt criteriile de atribuire?"
    print(f"\nQuerying for: '{query}'")

    results = vectorstore.similarity_search(query, k=2)

    print(f"\nFound {len(results)} relevant chunks:\n")
    for i, res in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(res.page_content)
        print("------------------\n")

if __name__ == "__main__":
    main()
