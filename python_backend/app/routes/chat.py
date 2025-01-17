import logging
from typing import List


from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.exceptions import HTTPException

from crud import chat as chat_crud
from crud import user as user_crud
from models import Chat
from schemas import chat as chat_schema

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/chat',
    
    tags=['chat']
)


@router.get(
    path='',
    response_model=List[chat_schema.ReadChat]
)
def get_chats(
    request: Request,
    params: chat_schema.GetChatsParams = Depends(),
):
    """ Get all public chats or search by name. """
    chats = chat_crud.get_chats(request.state.db, params)
    #result = [
    #    chat_schema.ReadChat(
    #        id=chat.id,
    #        name=chat.name,
    #        description=chat.description,
    #        is_private=chat.is_private,
    #        chat_owner=chat.chat_owner,
    #        created_at=chat.created_at,
    #        updated_at=chat.updated_at,
    #        users=[
    #            {"id": user.id, "username": user.username} for user in chat.users
    #        ],
    #    )
    #    for chat in chats
    #]
    
    return chats


@router.get(
    path='/{chat_id}',
    response_model=List[chat_schema.ReadChat]
)
def get_chat(
    request: Request,
    chat_id: int
):
    """ Get chat by chat id. """
    logger.info('Get chat by id: %s', chat_id)
    current_user = user_crud.get_user_by_name(request.state.db, request.state.username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    chat = chat_crud.get_chat_by_id(request.state.db, chat_id)
    if not chat or current_user not in chat.users:
        raise HTTPException(
            status_code=403,
            detail="Chat not found or access denied."
        )

    return chat


@router.post(
    path='',
    response_model=chat_schema.ReadChat
)
def post_chat(
    request: Request,
    chat_data: chat_schema.CreateChat
):
    current_user = user_crud.get_user_by_name(request.state.db, request.state.username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    new_chat = Chat(
        chat_data.name,
        chat_data.description,
        chat_data.is_private,
    )
    new_chat.chat_owner = current_user
    new_chat.chat_owner_id = current_user.id
    logger.info('New chat: %s', new_chat)

    logger.info('Add to db: %s', new_chat)
    request.state.db.add(new_chat)
    logger.info('Commit')
    request.state.db.commit()
    logger.info('Refresh')
    request.state.db.refresh(new_chat)
    logger.info('New chat: %s', new_chat)
    return new_chat


@router.patch(
    path='/{chat_id}',
    response_model=chat_schema.ReadChat
)
def patch_chat(
    chat_id: str,
    request: Request,
    chat_data: chat_schema.CreateChat
):
    logger.info('Patch chat, id: %s', chat_id)
    current_user = user_crud.get_user_by_name(request.state.db, request.state.username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    
    existing_chat = chat_crud.get_chat_by_id(request.state.db, chat_id)
    if not existing_chat or existing_chat.chat_owner_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Chat not found or invalid permissions."
        )
    
    for var, value in vars(chat_data).items():
        setattr(existing_chat, var, value) if value is not None else None

    logger.info('Add to db: %s', existing_chat)
    request.state.db.add(existing_chat)
    logger.info('Commit')
    request.state.db.commit()
    logger.info('Refresh')
    request.state.db.refresh(existing_chat)
    logger.info('New chat: %s', existing_chat)
    return existing_chat

