from fastapi import APIRouter

from pydantic import BaseModel

from app.services.flashcard_generator import (
    generate_flashcards
)

router = APIRouter()


class FlashcardRequest(BaseModel):

    topic: str
    num_cards: int = 5


@router.post("/generate-flashcards")
async def create_flashcards(
    request: FlashcardRequest
):

    flashcards = generate_flashcards(
        topic=request.topic,
        num_cards=request.num_cards
    )

    return {
        "topic": request.topic,
        "flashcards": flashcards
    }