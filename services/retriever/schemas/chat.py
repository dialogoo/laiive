from pydantic import BaseModel
from typing import Optional


class DataRange(BaseModel):
    start: str
    end: str


class SQLFilter(BaseModel):
    date_range: Optional[DataRange] = None
    place: Optional[str] = None


class ChatRequest_manual(BaseModel):
    message: str
    filters: dict


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
