from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.ingestion import ingestion_service
from app.services.vector_db import vector_db_service

router = APIRouter()

class ScrapeRequest(BaseModel):
    client_id: str
    url: HttpUrl

class FAQRequest(BaseModel):
    client_id: str
    question: str
    answer: str

@router.post("/scrape")
def scrape_website(request: ScrapeRequest):
    """Trigger scraper, chunk text, and embed into ChromaDB."""
    try:
        result = ingestion_service.process_website(str(request.url), request.client_id)
        return {"message": f"Successfully scraped and embedded {request.url}", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/faq")
def add_faq(request: FAQRequest):
    """Store FAQ direct to ChromaDB."""
    try:
        result = ingestion_service.process_faq(request.question, request.answer, request.client_id)
        return {"message": "FAQ successfully embedded", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_knowledge(query: str, client_id: str):
    """Test endpoint to search vector context given a prompt and client_id."""
    try:
        results = vector_db_service.search_similar(query, client_id=client_id, n_results=3)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
