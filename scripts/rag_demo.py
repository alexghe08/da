import os
import sys
import re
from typing import List
from dotenv import load_dotenv

# Add backend to sys path to ensure we can import if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../backend/.env'))

def split_by_article(text: str) -> List[str]:
    """
    Splits the text into chunks based on 'Articolul X'.
    Uses regex lookahead to keep the 'Articolul X' header with the content.
    """
    # Pattern: Split on newline followed by 'Articolul' and a number
    # We use a capturing group or just split.
    # re.split with capturing group keeps the delimiter if we are not careful.
    # Here we can just find all matches and their indices, or use a positive lookahead split.

    # Simple approach: split by the lookahead.
    # Note: re.split with zero-width match might behave differently in some python versions or produce empty strings.
    # Let's use a more manual approach to be safe and clear.

    pattern = r"\n(?=Articolul \d+)"
    chunks = re.split(pattern, text)
    # Filter out empty chunks and strip whitespace
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def main():
    print("--- LicitatieAI RAG Demo (Semantic Chunking) ---")

    # 1. Load Data
    file_path = os.path.join(os.path.dirname(__file__), '../data/legislation/sample_law.txt')
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print(f"Loading law text from: {file_path}")
    loader = TextLoader(file_path)
    raw_documents = loader.load()
    full_text = "\n\n".join([d.page_content for d in raw_documents])
    print(f"Loaded text length: {len(full_text)} characters.")

    # 2. Split Data Semantically (by Article)
    text_chunks = split_by_article(full_text)

    # Convert back to Documents
    documents = [Document(page_content=chunk, metadata={"source": file_path}) for chunk in text_chunks]

    print(f"Split into {len(documents)} semantic chunks (Articles).")

    # Debug: Print first 50 chars of each chunk to verify
    for i, doc in enumerate(documents[:3]):
        print(f"Chunk {i+1} starts with: {doc.page_content[:50].replace(chr(10), ' ')}...")

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
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)

    # 5. Query
    query = "Care sunt criteriile de atribuire?"
    print(f"\nQuerying for: '{query}'")

    results = vectorstore.similarity_search(query, k=2)

    print(f"\nFound {len(results)} relevant chunks:\n")
    for i, res in enumerate(results):
        print(f"--- Result {i+1} ---")
        # Print first 200 chars to show it's the right article
        print(res.page_content)
        print("------------------\n")

if __name__ == "__main__":
    main()
