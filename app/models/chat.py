from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    client_id: str = Field(..., description="Unique identifier for the client")
    session_id: str = Field(..., description="Unique identifier for the chat session")
    message: str = Field(..., description="The user's query or message")

class ChatResponse(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    reply: str = Field(..., description="The response reply message from the bot")
    lead_capture_prompt: bool = Field(False, description="Flag indicating whether to display a lead capture form to the user")

class LeadCaptureRequest(BaseModel):
    client_id: str = Field(..., description="Unique identifier for the client")
    session_id: str = Field(..., description="Unique identifier for the chat session")
    email: str = Field(..., description="Lead email address")
    unresolved_question: str = Field(..., description="The user's query that triggered the fallback")

class UnresolvedQuery(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    query: str = Field(..., description="The query that could not be resolved by the chatbot")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the query was recorded")
