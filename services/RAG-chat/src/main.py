from loguru import logger
from fastapi import FastAPI, status
from src.config import get_settings


# get the settings
settings = get_settings()

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


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RAG-chat server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec
    logger.info("RAG-chat server started")
