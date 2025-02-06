import logging
from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.database import get_db
from schemas import user as schema, auth as auth_schema, friend_request, chatbot
from schemas.general import PaginationParams
from crud import user as crud 
from core.authentication import authenticate_user
from core.models import User

logger = logging.getLogger('uvicorn')


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(authenticate_user)]
)


@router.get(
    path='/me',
    response_model=schema.ReadUser
)
async def get_me(
    current_user: User = Depends(authenticate_user),
):
    """ Get current user. """
    logger.info('Get current user: %s', current_user)

    return current_user


@router.get(
    path='',
    response_model=List[schema.ReadUser]
)
async def get_users(
    pagination: PaginationParams,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Get all users. """
    logger.info('Get all users.')

    # Waiting for admin roles
    #if True:
    #    raise HTTPException(403, 'Insufficient permissions')

    users = await crud.get_all_users(db_session, pagination)

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users found",
        )

    return users


@router.get(
    path='/{user_id}',
    response_model=schema.ReadUser
)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Get user by id. """
    logger.info('Get user by id.')

    #current_user = await crud.get_user_by_name(request.state.db, username)
    
    # Admin check here
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )
    
    user = await crud.get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(
                status_code=403,
                detail="User not found",
            )

    return user

"""
@router.post(
    path='',
    response_model=schema.ReadUser
)
async def create_user(
    request: Request,
    new_user_data: auth_schema.RegisterUser,
    username=Depends(authenticate_user)
):
    logger.info('Create new user.')
    
    current_user = await crud.get_user_by_name(request.state.db, username)

    # Waiting for admin stuff
    #if True:
    #    raise HTTPException(
    #        status_code=403,
    #        detail="Insufficient permissions",
    #    )

    if current_user:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )

    # Check if the username or email already exists
    existing_username = await crud.get_user_by_name(request.state.db, new_user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken",
        )

    existing_email = await crud.get_user_by_email(request.state.db, new_user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already taken",
        )

    user = await crud.create_user(request.state.db, new_user_data)

    # Commit the new user to the database
    await request.state.db.commit()
    await request.state.db.refresh(user)

    logger.info("Returning new user: %s", user)
    return user
"""

@router.patch(
    path='/{user_id}',
    response_model=schema.ReadUser
)
async def patch_user(
    user_id: int,
    user_data: schema.PatchUser,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Patch user by id. """
    logger.info('Patch user.')

    # Admin check here
    if current_user.id != user_id:
        raise HTTPException(
            status_code=404,
            detail="User not found or invalid permissions.",
        )

    patched_user = await crud.patch_user(db_session, user_id, user_data)

    logger.info('Updated user: %s', patched_user)
    return patched_user


@router.delete(
    path='/{user_id}',
    response_model=schema.ReadUser
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    """ Delete a user by id. """
    logger.info('Delete user by id.')

    # Admin check here
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User not found or invalid permissions",
        )
    
    deleted_user = await crud.delete_user(db_session, user_id)

    logger.info("Deleted user: %s", deleted_user)
    return deleted_user

###########################################
#                 Friends                 #
###########################################

@router.get(
    path="/{user_id}/friends",
    response_model = List[schema.ReadUser]
)
async def get_friends(
    user_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    user_friends = await crud.get_user_with_friends(db_session, user_id)
    logger.info('User friends: %s', user_friends.friends)
    if not user_friends:
        raise HTTPException(404, 'Friends not found.')

    return user_friends.friends


@router.get(
    path="/{user_id}/friend-requests",
    response_model = friend_request.FriendRequestResponse
)
async def get_friend_requests(
    user_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")
    
    logger.info('Getting friend requests!')
    
    friend_requests = await crud.get_friend_requests(db_session, user_id)

    return {'friend_requests': friend_requests}


@router.post(
    path="/{user_id}/friend-requests",
    response_model=friend_request.FriendRequestResponse
)
async def send_friend_request(
    user_id: int, 
    friend_request: friend_request.FriendRequestCreate, 
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    new_request = await crud.create_friend_request(db_session, sender_id=current_user.id, username=friend_request.username)
    return new_request


@router.post(
    path="/{user_id}/friend-requests/{request_id}/accept",
    response_model=friend_request.FriendRequest,
    #status_code=201
)
async def accept_friend_request(
    user_id: int, 
    request_id: int, 
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    logger.info('Accepting friend request!')
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    accepted_request = await crud.accept_friend_request(db_session, user_id=current_user.id, request_id=request_id)
    logger.info('Accepted request: %s', accepted_request)
    return accepted_request


@router.post(
    path="/{user_id}/friend-requests/{request_id}/reject",
    response_model=friend_request.FriendRequestResponse
)
async def reject_friend_request(
    user_id: int,
    request_id: int,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    try:
        rejected_request = await crud.reject_friend_request(db_session, user_id=current_user.id, request_id=request_id)
    except Exception as e:
        logger.error('Failed to accept friendship')
        logger.exception(e)
        raise e
    return rejected_request


###########################################
#                ChatBots                 #
###########################################
# Need to refactor these at some point!!

@router.get(
    path='/{user_id}/chatbots'
)
async def get_chatbots(
    user_id: str,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    logger.info('Get user %s chatbots', user_id)

    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    chatbots = await crud.get_user_chatbots(db_session, user_id)

    return chatbots


@router.post(
    path='/{user_id}/chatbots',
    response_model=chatbot.ReadChatBot
)
async def get_chatbots(
    user_id: str,
    bot_data: chatbot.CreateChatBot,
    current_user: User = Depends(authenticate_user),
    db_session: AsyncSession = Depends(get_db)
):
    logger.info('Post user %s chatbot', user_id)

    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Invalid permissions or user not found")

    chatbots = await crud.create_user_chatbots(db_session, current_user, bot_data)

    return chatbots