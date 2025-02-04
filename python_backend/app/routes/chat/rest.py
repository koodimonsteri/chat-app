import logging
from typing import List


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from core.authentication import authenticate_user
from core.database import get_db
from crud import chat as chat_crud
from crud import user as user_crud
#from models import Chat
from schemas import chat as chat_schema
from core.models import User

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/chats',
    tags=['chats'],
    dependencies=[Depends(authenticate_user)]
)


@router.get(
    path='',
    response_model=List[chat_schema.ReadChat]
)
async def get_chats(
    params: chat_schema.GetChatsParams = Depends(),
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Get public chats or search by name. """
    logger.info('Get chats with params: %s', params)
    if params.current_user:
        chats = await chat_crud.get_current_user_chats(db_session, current_user)
    else:
        chats = await chat_crud.get_chats(db_session, params)
    
    return chats


@router.get(
    path='/{chat_id}',
    response_model=List[chat_schema.ReadChat]
)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Get chat by chat id. """
    logger.info('Get chat by id: %s', chat_id)

    chat = await chat_crud.get_chat_by_id(db_session, chat_id)
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
async def post_chat(
    chat_data: chat_schema.CreateChat,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Create new chat. """
    logger.info('Create new chat: %s', chat_data)
    new_chat = await chat_crud.create_chat(db_session, current_user, chat_data)
    return new_chat


@router.patch(
    path='/{chat_id}',
    response_model=chat_schema.ReadChat
)
async def patch_chat(
    chat_id: str,
    chat_data: chat_schema.CreateChat,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Patch chat by chat id. """
    logger.info('Patch chat, id: %s', chat_id)
    
    # TODO username and password ??
    patched_chat = await chat_crud.patch_chat(db_session, current_user, chat_id, chat_data)
    
    return patched_chat


@router.delete(
    path="/{chat_id}",
    response_model=chat_schema.ReadChat
)
async def delete_chat_endpoint(
    chat_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """Delete a chat by chat id."""

    logger.info('Delete chat by id: %s', chat_id)
    deleted_chat = await chat_crud.delete_chat(db_session, chat_id, current_user.id)

    return deleted_chat