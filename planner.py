import os

from fastapi import APIRouter

from pydantic import BaseModel

from app.services.topic_extractor import (
    extract_topics
)

from app.services.pyq_analyzer import (
    analyze_pyqs
)

from app.services.importance_ranker import (
    rank_topics
)

from app.services.study_planner import (
    generate_study_plan
)

router = APIRouter()

PROCESSED_DIR = "app/data/processed"


class PlannerRequest(BaseModel):

    exam_date: str
    hours_per_day: int


@router.post("/generate-study-plan")
async def create_study_plan(
    request: PlannerRequest
):

    combined_text = ""

    for file in os.listdir(PROCESSED_DIR):

        path = os.path.join(
            PROCESSED_DIR,
            file
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            combined_text += f.read()

    if len(combined_text) > 20000:
        combined_text = combined_text[:20000]

    note_topics = extract_topics(
        combined_text
    )

    pyq_topics = analyze_pyqs(
        combined_text
    )

    ranked_topics = rank_topics(
        note_topics,
        pyq_topics
    )

    study_plan = generate_study_plan(
        ranked_topics,
        request.exam_date,
        request.hours_per_day
    )

    return {
        "ranked_topics": ranked_topics,
        "study_plan": study_plan
    }