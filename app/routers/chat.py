from fastapi import APIRouter
from datetime import datetime
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_advisor import generate_chat_reply

router = APIRouter(tags=["AI Clinical Assistant"])

@router.post("/chat", response_model=ChatResponse)
def chat_advisory(payload: ChatRequest):
    reply_text = generate_chat_reply(payload.message, payload.context)
    return ChatResponse(
        reply=reply_text,
        timestamp=datetime.now().strftime("%I:%M %p")
    )
