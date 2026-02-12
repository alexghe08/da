# LicitatieAI - Technical Architecture Analysis

Based on the patent draft provided, **LicitatieAI** is an intelligent platform for automating the generation of public procurement documents. Below is a technical breakdown of the system components and a proposed implementation stack.

## 1. System Overview

The platform automates the creation of legal documents (e.g., *Caiet de sarcini*, *Fișa de date*, *Contract*) by combining:
- **User Input**: Structured forms.
- **Document Extraction**: Analyzing existing PDFs (e.g., previous similar tenders).
- **RAG (Retrieval-Augmented Generation)**: Consulting a legal knowledge base (laws, HG, templates).
- **Generative AI**: Writing the content using an LLM.
- **Synchronization**: Ensuring data consistency across all documents in a packet.

## 2. Core Modules

### A. Input & Data Management
- **Function**: Collects metadata (Project Title, Budget, CPV Codes) and uploads files.
- **Key Feature**: A central database stores "Key Facts" (e.g., Budget = 100k RON). If this fact changes, it propagates to all generated documents.

### B. Semantic PDF Extraction Engine
- **Input**: User-uploaded PDFs/DOCX (e.g., "Referat de necesitate").
- **Process**:
  1.  **OCR/Text Extraction**: Convert binary files to text.
  2.  **Semantic Parsing**: Identify sections (Budget, Technical Specs, Deadlines).
  3.  **Structured Output**: JSON object to pre-fill the form.
- **Tech**: `PyPDF2`, `Tesseract` (OCR), or LLM-based parsers (e.g., `LlamaParse`).

### C. Knowledge Base (RAG)
- **Content**:
  - *Legislation*: Public Procurement Law (Legea 98/2016), Government Decisions (HG).
  - *Templates*: Standardized contracts, best practice guides.
- **Mechanism**: Hybrid Search (Vector Semantic Search + Keyword Search) to find relevant clauses based on the section being generated.

### D. Generative AI Engine
- **Role**: Generates the actual text for document sections.
- **Flow**: `Prompt` = `System Instructions` + `User Data` + `Extracted PDF Info` + `RAG Context`.
- **Validation**: Checks generated citations against the actual legal corpus.

### E. Synchronization Engine
- **Logic**: A listener/observer pattern. When a "Key Fact" is updated in the UI or one document, the system identifies all dependent documents and triggers a regeneration or specific field update.

## 3. Proposed Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Backend** | **Python (FastAPI)** | High performance, excellent ecosystem for AI/LLM libraries. |
| **Frontend** | **React / Next.js** | Interactive UI for form filling and document preview. |
| **LLM Orchestration** | **LangChain** or **LlamaIndex** | Standard for building RAG pipelines. |
| **LLM Provider** | **OpenAI (GPT-4o)** or **Anthropic (Claude 3.5)** | High capability for legal/Romanian text generation. |
| **Vector Database** | **ChromaDB** or **Qdrant** | Storing embeddings for the legal corpus. |
| **Main Database** | **PostgreSQL** | Relational data for users, projects, and structured "Key Facts". |
| **PDF Processing** | **Unstructured** / **PyMuPDF** | Robust text extraction from documents. |

## 4. Development Roadmap

1.  **Project Scaffolding**: Setup repo, backend/frontend folders.
2.  **Database Design**: Define schemas for `Project`, `Document`, `KeyFact`, `KnowledgeChunk`.
3.  **RAG Pipeline**: Ingest Romanian procurement laws into a vector store.
4.  **PDF Extractor**: Build a script to parse a sample "Referat de necesitate".
5.  **Generator API**: Endpoint that accepts JSON context and returns a drafted document section.
6.  **UI Implementation**: Dashboard for managing projects and viewing generated docs.
