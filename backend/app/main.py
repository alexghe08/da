from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager
import os

# Import the RAG engine
# Using relative import assuming this is run as a module or package
from .rag_engine import rag_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load knowledge base on startup
    # We assume the data directory is relative to the project root
    # Adjust path if necessary. backend/app/main.py -> ../../data/legislation
    data_path = os.path.join(os.path.dirname(__file__), '../../data/legislation')
    rag_engine.initialize_knowledge_base(data_path)
    yield
    # Clean up resources if needed

app = FastAPI(
    title="LicitatieAI API",
    description="API for generating public procurement documents",
    lifespan=lifespan
)

class GenerateRequest(BaseModel):
    document_type: str  # e.g., "caiet_sarcini", "fisa_date"
    project_title: str
    section: Optional[str] = "General"
    context_data: Optional[dict] = Field(default_factory=dict)

class GenerateResponse(BaseModel):
    content: str
    source_references: list[str]

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LicitatieAI Backend"}

@app.post("/generate", response_model=GenerateResponse)
def generate_document_section(request: GenerateRequest):
    """
    Generates a document section using RAG.
    """
    topic = f"{request.section} - {request.project_title}"

    # 1. Retrieve Context
    print(f"Retrieving context for: {topic}")
    context_docs = rag_engine.retrieve_context(topic)

    # 2. Extract Sources for response
    sources = [doc.metadata.get("source", "Unknown") for doc in context_docs]
    # Deduplicate sources
    sources = list(set(sources))

    # 3. Generate Content
    print("Generating content...")
    content = rag_engine.generate_completion(
        topic=topic,
        context_docs=context_docs,
        document_type=request.document_type
    )

    return GenerateResponse(content=content, source_references=sources)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
