from fastapi import APIRouter
from pydantic import BaseModel
from app.services.summary_generator import generate_topic_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    topic: str

@router.post("/generate-summary")
async def get_summary(request: SummaryRequest):
    summary_text = generate_topic_summary(request.topic)
    return {"summary": summary_text}
