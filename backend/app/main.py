from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager
import os
import tempfile
from docxtpl import DocxTemplate

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

class DocGenRequest(BaseModel):
    template_name: str  # e.g., "fisa_date.docx"
    context_data: dict = Field(default_factory=dict)

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

@app.post("/generate-document")
def generate_document_file(request: DocGenRequest):
    """
    Generates a complete .docx file from a template.
    """
    template_path = os.path.join(os.path.dirname(__file__), '../../data/templates', request.template_name)

    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail=f"Template {request.template_name} not found.")

    try:
        doc = DocxTemplate(template_path)
        doc.render(request.context_data)

        # Save to a temporary file
        temp_dir = tempfile.gettempdir()
        output_filename = f"generated_{request.template_name}"
        output_path = os.path.join(temp_dir, output_filename)
        doc.save(output_path)

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
