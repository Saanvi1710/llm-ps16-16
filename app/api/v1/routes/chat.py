from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.messages import add_message, get_history
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat_service
from app.services.personas import PERSONAS

router = APIRouter(prefix="/chat", tags=["chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/figures")
def list_figures() -> dict[str, list[str]]:
    return {"figures": list(PERSONAS)}


@router.post("", response_model=ChatResponse)
def send_message(
    payload: ChatRequest,
    db: Annotated[Session, Depends(get_db)],
) -> ChatResponse:
    if payload.figure not in PERSONAS:
        raise HTTPException(status_code=422, detail="Choose a supported historical figure.")

    conversation_id = str(payload.conversation_id)
    history = [
        {"role": item.role, "content": item.content}
        for item in get_history(db, conversation_id, payload.figure)
    ]
    try:
        reply = chat_service.reply(payload.figure, history, payload.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    add_message(db, conversation_id, payload.figure, "user", payload.message)
    add_message(db, conversation_id, payload.figure, "assistant", reply)
    return ChatResponse(figure=payload.figure, reply=reply)
