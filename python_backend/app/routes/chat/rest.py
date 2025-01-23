import logging
from typing import List


from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.exceptions import HTTPException

from crud import chat as chat_crud
from crud import user as user_crud
#from models import Chat
from schemas import chat as chat_schema
from authentication import authenticate_user

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/chat',
    tags=['chat'],
    dependencies=[Depends(authenticate_user)]
)


@router.get(
    path='',
    response_model=List[chat_schema.ReadChat]
)
async def get_chats(
    request: Request,
    params: chat_schema.GetChatsParams = Depends(),
    username = Depends(authenticate_user)
):
    """ Get public chats or search by name. """
    logger.info('Get chats with params: %s', params)
    if params.current_user:
        current_user = await user_crud.get_user_by_name(request.state.db, username)
        chats = await chat_crud.get_current_user_chats(request.state.db, current_user)
    else:
        chats = await chat_crud.get_chats(request.state.db, params)
    
    return chats


@router.get(
    path='/{chat_id}',
    response_model=List[chat_schema.ReadChat]
)
async def get_chat(
    request: Request,
    chat_id: int,
    username = Depends(authenticate_user)
):
    """ Get chat by chat id. """
    logger.info('Get chat by id: %s', chat_id)
    current_user = await user_crud.get_user_by_name(request.state.db, username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    chat = await chat_crud.get_chat_by_id(request.state.db, chat_id)
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
    request: Request,
    chat_data: chat_schema.CreateChat,
    username = Depends(authenticate_user)
):
    """ Create new chat. """
    current_user = await user_crud.get_user_by_name(request.state.db, username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    
    new_chat = await chat_crud.create_chat(request.state.db, current_user, chat_data)
    
    return new_chat


@router.patch(
    path='/{chat_id}',
    response_model=chat_schema.ReadChat
)
async def patch_chat(
    chat_id: str,
    request: Request,
    chat_data: chat_schema.CreateChat,
    username = Depends(authenticate_user)
):
    """ Patch chat by chat id. """
    logger.info('Patch chat, id: %s', chat_id)
    current_user = await user_crud.get_user_by_name(request.state.db, username)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    
    existing_chat = await chat_crud.get_chat_by_id(request.state.db, chat_id)
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
    await request.state.db.commit()
    logger.info('Refresh')
    await request.state.db.refresh(existing_chat)
    logger.info('New chat: %s', existing_chat)
    return existing_chat


