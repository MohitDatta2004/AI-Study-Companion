from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.upload import router as upload_router
from app.api.retrieval import router as retrieval_router
from app.api.chatbot import router as chatbot_router
from app.api.quiz import router as quiz_router
from app.api.flashcards import router as flashcards_router
from app.api.topics import router as topics_router
from app.api.planner import router as planner_router
from app.api.mindmap import router as mindmap_router
from app.api.summary import router as summary_router

app = FastAPI(
    title="StudyGenie AI",
    version="1.0.0",
    openapi_version="3.0.2"
)

app.include_router(upload_router)
app.include_router(retrieval_router)
app.include_router(chatbot_router)
app.include_router(quiz_router)
app.include_router(flashcards_router)
app.include_router(topics_router)
app.include_router(planner_router)
app.include_router(mindmap_router)
app.include_router(summary_router)

def fix_schema_recursive(obj: dict) -> None:
    if isinstance(obj, dict):
        if obj.get("contentMediaType") == "application/octet-stream":
            del obj["contentMediaType"]
            obj["type"] = "string"
            obj["format"] = "binary"
        for value in obj.values():
            fix_schema_recursive(value)
    elif isinstance(obj, list):
        for item in obj:
            fix_schema_recursive(item)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    fix_schema_recursive(openapi_schema)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    return {"message": "StudyGenie AI Backend Running"}