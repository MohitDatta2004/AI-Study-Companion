from fastapi import APIRouter
from pydantic import BaseModel
from app.services.mindmap_generator import generate_mindmap

router = APIRouter()

class MindmapRequest(BaseModel):
    topic: str

@router.post("/generate-mindmap")
async def generate_mindmap_endpoint(request: MindmapRequest):
    mermaid_code = generate_mindmap(request.topic)
    return {"topic": request.topic, "mermaid_code": mermaid_code}
