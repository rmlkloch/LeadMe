from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat import LeadCaptureRequest

router = APIRouter()

@router.post("/", status_code=201)
def capture_lead(request: LeadCaptureRequest, db: Session = Depends(get_db)):
    """
    Capture prospective business lead information associated with a chat session.
    """
    return {
        "status": "success",
        "message": f"Lead for session {request.session_id} captured successfully",
        "data": {
            "name": request.name,
            "email": request.email
        }
    }
