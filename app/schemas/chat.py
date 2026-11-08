from typing import Optional, Dict, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    timestamp: str
