# LicitatieAI

**Platformă inteligentă pentru generarea automată a documentației de licitație publică asistată de AI.**

## Descriere

LicitatieAI este o soluție software avansată care automatizează procesul de creare a documentelor necesare în procedurile de achiziții publice (ex: Caiet de sarcini, Fișa de date, Contract). Platforma utilizează tehnologii de Inteligență Artificială Generativă (LLM) și Regăsire Augmentată a Informației (RAG) pentru a asigura conformitatea legală și coerența datelor între documente.

## Funcționalități Cheie

1.  **Generare Asistată de AI**: Crearea automată a textului pentru secțiuni specifice din documente, bazat pe legislația în vigoare.
2.  **RAG Juridic**: Integrarea cu o bază de cunoștințe legislativă (Legea 98/2016, HG-uri) pentru a oferi referințe corecte.
3.  **Extragere din PDF**: Analiza documentelor anterioare (ex: Referat de necesitate) pentru a pre-completa datele noii proceduri.
4.  **Sincronizare Automată**: Modificarea unei informații (ex: buget, termen) într-un document se propagă automat în toate celelalte documente asociate.

## Arhitectură (Propusă)

*   **Backend**: Python (FastAPI / Django)
*   **Frontend**: React / Next.js
*   **AI Engine**: LangChain / LlamaIndex + OpenAI/Anthropic
*   **Database**: PostgreSQL + Vector DB (Chroma/Qdrant)

## Structura Proiectului

*   `docs/`: Documentație tehnică și specificații (inclusiv draftul de brevet).
*   `backend/`: API și logica de business.
*   `frontend/`: Interfața utilizator.
*   `data/`: Scripturi pentru procesarea datelor și a corpusului legislativ.

---
*Acest proiect este în faza de dezvoltare inițială, bazat pe specificațiile tehnice furnizate.*
