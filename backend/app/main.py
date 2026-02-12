from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="LicitatieAI API", description="API for generating public procurement documents")

class GenerateRequest(BaseModel):
    document_type: str  # e.g., "caiet_sarcini", "fisa_date"
    project_title: str
    section: Optional[str] = None
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
    Mock endpoint to generate a document section.
    In a real scenario, this would:
    1. Retrieve context from Vector DB (RAG).
    2. Call LLM with the prompt.
    3. Return the generated text.
    """

    # Mock Logic
    if request.document_type == "caiet_sarcini" and "obiect" in (request.section or "").lower():
        content = (
            f"OBIECTUL ACHIZIȚIEI: {request.project_title}\n\n"
            "Autoritatea contractantă dorește să achiziționeze servicii de înaltă calitate "
            "în conformitate cu specificațiile tehnice anexate. "
            "Prezentul Caiet de Sarcini face parte integrantă din documentația de atribuire..."
        )
        sources = ["Legea 98/2016 Art. 155"]
    else:
        content = (
            f"Aceasta este o secțiune generată automat pentru {request.document_type} "
            f"pentru proiectul '{request.project_title}'."
        )
        sources = ["General Template"]

    return GenerateResponse(content=content, source_references=sources)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
