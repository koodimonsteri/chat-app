import logging

from sqlalchemy import asc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from core.exceptions import ResourceNotFoundError, ResoureExists
from core.models import Chat, User
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
    query = select(Chat).options(joinedload(Chat.users)).where(Chat.id == chat_id)

    result = await db.execute(query)
    return result.unique().scalars().one_or_none()


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
    
    current_user_chats = await get_current_user_chats(db, current_user)
    if any([x.name == chat_data.name for x in current_user_chats]):
        raise ResoureExists(f'Chat exists already: {chat_data.name}')

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


async def patch_chat(db: AsyncSession, current_user, chat_id, chat_data: chat_schema.CreateChat):
    existing_chat = await get_chat_by_id(db, chat_id)
    if not existing_chat or existing_chat.chat_owner_id != current_user.id:
        raise ResourceNotFoundError("Chat not found or access denied.")
    
    for var, value in vars(chat_data).items():
        setattr(existing_chat, var, value) if value is not None else None

    db.add(existing_chat)
    await db.commit()
    await db.refresh(existing_chat)
    return existing_chat


async def delete_chat(db: AsyncSession, chat_id: int, current_user_id: int):
    chat = await get_chat_by_id(db, chat_id)
    
    if not chat or chat.chat_owner_id != current_user_id:
        raise ResourceNotFoundError("Chat not found or invalid permissions")
    
    #if chat.chat_owner_id != current_user_id:
    #    raise PermissionError("Invalid permissions to delete chat")
    
    await db.execute(delete(Chat).where(Chat.id == chat_id))
    await db.commit()

    return chat