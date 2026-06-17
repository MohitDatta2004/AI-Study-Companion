from fastapi import APIRouter

from app.services.retrieval_engine import (
    semantic_search
)

router = APIRouter()


@router.get("/search")
async def search_notes(
    query: str
):

    results = semantic_search(query)

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }