from fastapi import APIRouter
from app.api.v1.endpoints import chat, leads, knowledge, webhooks, tickets, system

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(system.router, prefix="/system", tags=["System"])

