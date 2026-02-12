import os
import re
from typing import List, Optional
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class RAGEngine:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.llm = None

    def initialize_knowledge_base(self, data_path: str = "data/legislation"):
        """
        Loads all text files from the data directory, splits them by article,
        and initializes the VectorStore.
        """
        print("Initializing Knowledge Base...")
        documents = []

        # 1. Load Documents
        if not os.path.exists(data_path):
            print(f"Warning: Data path {data_path} does not exist.")
            return

        for filename in os.listdir(data_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_path, filename)
                try:
                    loader = TextLoader(file_path)
                    raw_docs = loader.load()
                    for doc in raw_docs:
                        # 2. Semantic Split
                        chunks = self._split_by_article(doc.page_content)
                        for chunk in chunks:
                            documents.append(Document(page_content=chunk, metadata={"source": filename}))
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        if not documents:
            print("No documents found to index.")
            return

        print(f"Indexed {len(documents)} legal articles.")

        # 3. Embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and not api_key.startswith("your_"):
            embeddings = OpenAIEmbeddings()
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        else:
            print("WARNING: OPENAI_API_KEY not found. Using FakeEmbeddings and Mock LLM.")
            embeddings = FakeEmbeddings(size=1536)
            self.llm = None  # Will handle this in generate

        # 4. Vector Store
        # Using a transient in-memory store for this implementation
        self.vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        print("Knowledge Base Initialized.")

    def _split_by_article(self, text: str) -> List[str]:
        """
        Splits text by 'Articolul X'.
        """
        # Pattern: Newline followed by 'Articolul' and a number.
        # Uses positive lookahead to keep the delimiter.
        pattern = r"\n(?=Articolul \d+)"
        chunks = re.split(pattern, text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def retrieve_context(self, query: str) -> List[Document]:
        if not self.retriever:
            return []
        return self.retriever.invoke(query)

    def generate_completion(self, topic: str, context_docs: List[Document], document_type: str) -> str:
        """
        Generates the document section content using the LLM and retrieved context.
        """
        context_text = "\n\n".join([d.page_content for d in context_docs])

        if not self.llm:
            return (
                f"[MOCK GENERATION - NO API KEY]\n"
                f"Document Type: {document_type}\n"
                f"Topic: {topic}\n"
                f"Context Found:\n{context_text[:500]}..."
            )

        # Prompt Template
        template = """Ești un expert în achiziții publice din România. Sarcina ta este să redactezi o secțiune pentru un document de licitație.

        Tip Document: {document_type}
        Subiect: {topic}

        Folosește următoarele prevederi legale și informații de context pentru a formula textul:
        {context}

        Cerințe:
        1. Textul trebuie să fie formal, juridic și clar.
        2. Citează articolul de lege relevant dacă este cazul.
        3. Nu inventa informații care nu sunt susținute de lege sau de context.

        Redactează secțiunea acum:"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke({
            "document_type": document_type,
            "topic": topic,
            "context": context_text
        })

# Singleton instance
rag_engine = RAGEngine()
