from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def query_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Query the FAQ chatbot and get a response.
    """
    return ChatResponse(
        session_id=request.session_id,
        reply="This is a mock reply from LeadMe Chatbot. The backend foundation is successfully configured!",
        lead_capture_prompt=False
    )
