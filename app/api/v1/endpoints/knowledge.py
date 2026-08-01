from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.post("/ingest", status_code=202)
def ingest_document(title: str, content: str, source_url: str = None, db: Session = Depends(get_db)):
    """
    Ingest a new document/source into the knowledge base.
    """
    return {
        "status": "accepted",
        "message": f"Document '{title}' queued for processing and embedding."
    }
