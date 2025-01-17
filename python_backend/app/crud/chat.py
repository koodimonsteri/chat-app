import logging

from sqlalchemy import asc
from sqlalchemy.orm import Session

from models import Chat
from schemas import chat as chat_schema


def get_chats(db: Session, params: chat_schema.GetChatsParams):
    query = db.query(Chat).filter(Chat.is_private == False).all()

    if params.chat_name:
        query = query.filter(Chat.name.ilike(f"%{params.chat_name}%"))

    chats = (
        query.order_by(asc(Chat.created_at))
        .offset(params.start)
        .limit(params.limit)
    )
    return chats


def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).one_or_none()
