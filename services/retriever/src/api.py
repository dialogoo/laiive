from loguru import logger
from fastapi import FastAPI, status
from datetime import date
from pydantic import BaseModel
from typing import Optional
from src.config import settings
from src.main import get_response


# Schemas defined inline TODO if API endpoints > 15 move Schemas to schemas file.
class DataRange(BaseModel):
    start: date
    end: date


class SQLFilter(BaseModel):
    date_range: Optional[DataRange] = None
    place: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    filters: Optional[SQLFilter] = None


class ChatResponse(BaseModel):
    response: str


# Create the app
app = FastAPI(
    title="retriever",
    description="retriever service is the chat backend that queries laiive database to inform about musical life events",
    version="0.1.0",
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "msg": "retriever is running, healthy and ready to answer questions",
        "status": "healthy",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await get_response(request.message, request.filters)
    return ChatResponse(response=response)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting retriever server...")
    uvicorn.run(app, host=settings.host, port=settings.port)  # nosec
    logger.info("retriever server started")
