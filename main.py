from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.api import api_router

# Create Database tables on startup
Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Health Check",
        "description": "System health diagnostics.",
    },
    {
        "name": "Chat",
        "description": "FAQ query matching and bot response operations.",
    },
    {
        "name": "Leads",
        "description": "Lead capturing and retrieval endpoints.",
    },
    {
        "name": "Knowledge",
        "description": "CRUD for documents and scraping pipelines.",
    },
    {
        "name": "Webhooks",
        "description": "Handles notifications and external integrations.",
    }
]

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.reset import reset_demo_environment

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_demo_environment, 'interval', hours=12)
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="24/7 Lead Capture and FAQ Chatbot API Platform",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck endpoint
@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "LeadMe API is running"}

# Include API V1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)
