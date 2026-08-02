from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat import ChatRequest, ChatResponse
from app.services.llm import llm_service

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
def chat_message(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Core chat loop: receive message, search knowledge base, generate answer or fallback.
    """
    result = llm_service.generate_chat_response(query=request.message, client_id=request.client_id)
    
    print(f"--- DEBUG LLM RAW RESPONSE --- \n{result}\n------------------------------")
    
    if result.get("needs_fallback"):
        return ChatResponse(
            session_id=request.session_id,
            reply="I don't have enough information to answer that right now. Could you please provide your email so our staff can follow up with you?",
            lead_capture_prompt=True
        )
    
    return ChatResponse(
        session_id=request.session_id,
        reply=result.get("answer", ""),
        lead_capture_prompt=False
    )

