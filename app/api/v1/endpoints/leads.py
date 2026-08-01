from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat import LeadCaptureRequest
from app.models.db_models import Lead, Ticket
from app.services.notifications import notification_service

router = APIRouter()

@router.post("/capture", status_code=201)
def capture_lead(request: LeadCaptureRequest, db: Session = Depends(get_db)):
    """
    Capture prospective business lead information and open a support ticket.
    """
    try:
        # 1. Save Lead
        new_lead = Lead(
            client_id=request.client_id,
            session_id=request.session_id,
            email=request.email
        )
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        
        # 2. Save Ticket
        new_ticket = Ticket(
            client_id=request.client_id,
            lead_id=new_lead.id,
            question=request.unresolved_question
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        # 3. Notify Staff
        notification_service.notify_staff_of_ticket(
            ticket_id=new_ticket.id,
            client_id=request.client_id,
            question=request.unresolved_question,
            email=request.email
        )
        
        return {
            "status": "success",
            "message": "Lead captured and staff notified.",
            "ticket_id": new_ticket.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

