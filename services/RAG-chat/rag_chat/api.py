from loguru import logger
from fastapi import FastAPI, status
from pydantic import BaseModel
from rag_chat.config import settings
from rag_chat.main import get_response
from typing import Optional
from schemas.chat import (
    DataRange,
    SQLFilter,
    ChatRequest_manual,
    ChatRequest,
    ChatResponse,
)

# create the app
app = FastAPI(
    title="RAG-chat",
    description="RAG-chat is a Chatbot that uses RAG to answer questions about musical life events",
    version="0.1.0",
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "msg": "RAG-chat is running, healthy and ready to answer questions",
        "user": settings.postgres_user,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest_manual):
    filters_dict = request.filters

    date_range_obj = None
    if filters_dict.get("date_range"):
        date_range_dict = filters_dict["date_range"]
        date_range_obj = DataRange(
            start=date_range_dict["start"], end=date_range_dict["end"]
        )

    sql_filters = SQLFilter(date_range=date_range_obj, place=filters_dict.get("place"))

    response = await get_response(request.message, sql_filters)
    return ChatResponse(response=response)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RAG-chat server...")
    uvicorn.run(app, host=settings.host, port=settings.port)  # nosec
    logger.info("RAG-chat server started")
