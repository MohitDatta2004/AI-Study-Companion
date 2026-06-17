from fastapi import APIRouter

from pydantic import BaseModel

from app.services.rag_pipeline import (
    ask_studygenie
)

router = APIRouter()


class ChatRequest(BaseModel):

    question: str
    history: list = []


@router.post("/chat")
async def chat_with_notes(
    request: ChatRequest
):

    response = ask_studygenie(
        request.question,
        request.history
    )

    return response