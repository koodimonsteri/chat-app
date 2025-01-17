import logging

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from models import Chat, User
from schemas import chat as chat_schema


async def get_chats(db: AsyncSession, params: chat_schema.GetChatsParams):
    query = select(Chat).where(Chat.is_private == False)

    if params.chat_name:
        query = query.where(Chat.name.ilike(f"%{params.chat_name}%"))

    query = query.order_by(asc(Chat.created_at)).offset(params.start).limit(params.limit)

    query = query.options(joinedload(Chat.users))

    result = await db.execute(query)
    return result.unique().scalars().all()


async def get_chat_by_id(db: AsyncSession, chat_id: int):
    query = select(Chat).where(Chat.id == chat_id)

    result = await db.execute(query)
    return result.scalars().one_or_none()


async def get_current_user_chats(db: AsyncSession, current_user: User):
    result = await db.execute(
        select(Chat)
        .join(Chat.users)
        .filter(User.id == current_user.id)
        .options(joinedload(Chat.users))
    )
    chats = result.unique().scalars().all()
    return chats


async def create_chat(
    db: AsyncSession, 
    current_user: User, 
    chat_data: chat_schema.CreateChat
) -> Chat:
    """ Create and save a new chat to the database. """
    new_chat = Chat(
        name=chat_data.name,
        description=chat_data.description,
        is_private=chat_data.is_private,
        chat_owner=current_user,
        chat_owner_id=current_user.id
    )
    new_chat.users.append(current_user)

    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    chat_with_relations = await db.execute(
        select(Chat)
        .options(selectinload(Chat.chat_owner), selectinload(Chat.users))
        .where(Chat.id == new_chat.id)
    )
    chat_with_relations = chat_with_relations.scalar_one()
    return chat_with_relations
