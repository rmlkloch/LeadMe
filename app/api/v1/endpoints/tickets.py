from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import Ticket, Lead
from app.services.ingestion import ingestion_service
from app.services.notifications import notification_service

router = APIRouter()

class TicketResolveRequest(BaseModel):
    ticket_id: int
    answer: str

@router.post("/resolve")
def resolve_ticket(request: TicketResolveRequest, db: Session = Depends(get_db)):
    """
    Resolve a ticket and update vector memory with the new Q&A pair.
    """
    ticket = db.query(Ticket).filter(Ticket.id == request.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if ticket.status == "resolved":
        raise HTTPException(status_code=400, detail="Ticket is already resolved")

    # Fetch the lead to get their email
    lead = db.query(Lead).filter(Lead.id == ticket.lead_id).first()
    
    try:
        # 1. Update SQLite
        ticket.status = "resolved"
        db.commit()

        # 2. Add to Vector DB (so bot learns it forever)
        ingestion_service.process_faq(
            question=ticket.question,
            answer=request.answer,
            client_id=ticket.client_id
        )

        # 3. Notify the Lead
        if lead:
            notification_service.notify_lead_of_resolution(lead.email, request.answer)

        return {"status": "success", "message": f"Ticket {ticket.id} resolved and vector memory updated."}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
