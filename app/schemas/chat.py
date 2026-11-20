from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    figure: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=2_000)
    conversation_id: UUID


class ChatResponse(BaseModel):
    figure: str
    reply: str
