from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    message: str = Field(..., description="The user's query or message")

class ChatResponse(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    reply: str = Field(..., description="The response reply message from the bot")
    lead_capture_prompt: bool = Field(False, description="Flag indicating whether to display a lead capture form to the user")

class LeadCaptureRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    name: str = Field(..., description="Lead name")
    email: str = Field(..., description="Lead email address")
    phone: Optional[str] = Field(None, description="Lead contact phone number")
    company: Optional[str] = Field(None, description="Lead company name")
    notes: Optional[str] = Field(None, description="Additional context or notes about the lead")

class UnresolvedQuery(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    query: str = Field(..., description="The query that could not be resolved by the chatbot")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the query was recorded")
