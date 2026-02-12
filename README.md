# LicitatieAI

**Platformă inteligentă pentru generarea automată a documentației de licitație publică asistată de AI.**

## Descriere

LicitatieAI este o soluție software avansată care automatizează procesul de creare a documentelor necesare în procedurile de achiziții publice (ex: Caiet de sarcini, Fișa de date, Contract). Platforma utilizează tehnologii de Inteligență Artificială Generativă (LLM) și Regăsire Augmentată a Informației (RAG) pentru a asigura conformitatea legală și coerența datelor între documente.

## Funcționalități Cheie

1.  **Generare Asistată de AI**: Crearea automată a textului pentru secțiuni specifice din documente, bazat pe legislația în vigoare.
2.  **RAG Juridic**: Integrarea cu o bază de cunoștințe legislativă (Legea 98/2016, HG-uri) pentru a oferi referințe corecte.
3.  **Chunking Inteligent**: Algoritmi de segmentare semantică a textului legislativ (pe Articole/Capitole) pentru a menține contextul intact.
4.  **Extragere din PDF**: Analiza documentelor anterioare (ex: Referat de necesitate) pentru a pre-completa datele noii proceduri.

## Arhitectură (Propusă)

*   **Backend**: Python (FastAPI)
*   **AI Engine**: LangChain + OpenAI
*   **Database**: ChromaDB (Vector Store)

## Getting Started

### 1. Prerequisites
- Python 3.10+
- OpenAI API Key

### 2. Installation

```bash
# Clone repository
git clone <repo-url>
cd licitatieai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configuration

Create a `.env` file in `backend/` based on the example:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your OpenAI API Key:
```
OPENAI_API_KEY=sk-...
```

### 4. Running the API

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Documentation is available at `http://localhost:8000/docs`.

### 5. Testing Generation

You can use the `/generate` endpoint to create document sections.

**Example Request:**
```json
POST /generate
{
  "document_type": "caiet_sarcini",
  "project_title": "Renovare Scoala Generala Nr. 1",
  "section": "Obiectul contractului"
}
```
