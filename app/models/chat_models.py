# Pydantic models for chat interactions
from pydantic import BaseModel

class Message(BaseModel):
    id: str
    conversation_id: str
    sender: str # "user" or "ai"
    content: str
    timestamp: str # ISO format timestamp
