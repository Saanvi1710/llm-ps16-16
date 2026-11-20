from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


def add_message(
    db: Session, conversation_id: str, figure: str, role: str, content: str
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        figure=figure,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_history(db: Session, conversation_id: str, figure: str) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id, Message.figure == figure)
        .order_by(Message.id.desc())
        .limit(12)
    )
    return list(reversed(db.scalars(statement).all()))
