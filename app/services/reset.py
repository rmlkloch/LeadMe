import uuid
import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.db_models import Lead, Ticket
from app.services.vector_db import vector_db_service

logger = logging.getLogger(__name__)

def reset_demo_environment():
    """Reset the demo_client_1 environment."""
    client_id = "demo_client_1"
    logger.info(f"Starting automated reset for sandbox client: {client_id}")
    
    db: Session = SessionLocal()
    try:
        # a) Delete all records in SQLite for client_id == 'demo_client_1' in leads and tickets
        db.query(Ticket).filter(Ticket.client_id == client_id).delete(synchronize_session=False)
        db.query(Lead).filter(Lead.client_id == client_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Deleted SQLite records for {client_id}")

        # b) Clear vector memory
        vector_db_service.delete_knowledge_by_client(client_id)
        logger.info(f"Cleared ChromaDB vector memory for {client_id}")

        # c) Automatically re-seed default FAQ items
        default_faqs = [
            "We offer premium full-stack web development and AI integration services.",
            "Our operating hours are Monday through Friday, 9:00 AM to 5:00 PM EST.",
            "You can reach support directly at support@leadme.com."
        ]
        
        docs = []
        metas = []
        ids = []
        for faq in default_faqs:
            docs.append(faq)
            metas.append({"client_id": client_id, "type": "faq"})
            ids.append(str(uuid.uuid4()))
            
        vector_db_service.add_documents(documents=docs, metadatas=metas, ids=ids)
        logger.info(f"Re-seeded default FAQs for {client_id}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error resetting demo environment: {e}")
        raise e
    finally:
        db.close()
