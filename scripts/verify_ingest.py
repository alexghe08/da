import os
import sys

# Add backend to sys path to ensure we can import
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.rag_engine import rag_engine

def main():
    print("--- Verifying Knowledge Base Ingestion ---")
    data_path = os.path.join(os.path.dirname(__file__), '../data/legislation')

    # Run the initialization which prints the count of indexed articles
    rag_engine.initialize_knowledge_base(data_path)

    # Access the vectorstore to inspect documents if possible,
    # but the logs from initialize_knowledge_base should be sufficient.
    # We can also perform a quick retrieve to check content.

    print("\n--- Performing Test Retrieval ---")
    query = "praguri valorice"
    docs = rag_engine.retrieve_context(query)

    if docs:
        print(f"Successfully retrieved {len(docs)} documents for query '{query}'.")
        for i, doc in enumerate(docs):
            print(f"Result {i+1} Source: {doc.metadata.get('source')}")
            print(f"Preview: {doc.page_content[:100]}...\n")
    else:
        print("No documents retrieved. Ingestion might have failed.")

if __name__ == "__main__":
    main()
