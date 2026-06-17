from fastapi import APIRouter

from pydantic import BaseModel

from app.services.quiz_generator import (
    generate_quiz
)

router = APIRouter()


class QuizRequest(BaseModel):

    topic: str
    num_questions: int = 5


@router.post("/generate-quiz")
async def create_quiz(
    request: QuizRequest
):

    quiz = generate_quiz(
        topic=request.topic,
        num_questions=request.num_questions
    )

    return {
        "topic": request.topic,
        "quiz": quiz
    }