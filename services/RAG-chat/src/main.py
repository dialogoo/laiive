from loguru import logger
from fastapi import FastAPI, status
from pydantic import BaseModel
from src.config import settings
from src.rag import get_response

# create the app
app = FastAPI(
    title="RAG-chat",
    description="RAG-chat is a Chatbot that uses RAG to answer questions about musical life events",
    version="0.1.0",
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    filters: dict = {}

class ChatResponse(BaseModel):
    response: str


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "msg": "RAG-chat is running, healthy and ready to answer questions",
        "user": settings.postgres_user,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO: Implement actual RAG logic here
    filters_info = ""
    if request.filters:
        place = request.filters.get("place")
        date = request.filters.get("date")
        date_range = request.filters.get("date_range")

        if place:
            filters_info += f" in {place}"
        if date:
            filters_info += f" on {date}"
        if date_range:
            filters_info += f" between {date_range['start']} and {date_range['end']}"

    return ChatResponse(response=get_response(request.message, request.filters))


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RAG-chat server...")
    uvicorn.run(app, host=settings.host, port=settings.port)  # nosec
    logger.info("RAG-chat server started")
