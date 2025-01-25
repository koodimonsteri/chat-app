import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

#import jwt
#import settings
from schemas import user as schema, auth as auth_schema
from schemas.general import PaginationParams
from crud import user as crud 
from authentication import authenticate_user

logger = logging.getLogger('uvicorn')


router = APIRouter(
    prefix='/user',
    tags=['user'],
    dependencies=[Depends(authenticate_user)]
)


@router.get(
    path='/me',
    response_model=schema.ReadUser
)
async def get_me(
    request: Request,
    username = Depends(authenticate_user)
):
    """ Get current user. """
    user = await crud.get_user_by_name(request.state.db, username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.get(
    path='',
    response_model=List[schema.ReadUser]
)
async def get_users(
    request: Request,
    pagination: PaginationParams,
    username=Depends(authenticate_user)
):
    """ Get all users. """
    logger.info('Get all users.')

    # Waiting for admin roles
    if True:
        raise HTTPException(403, 'Insufficient permissions')

    users = await crud.get_all_users(request.state.db, pagination)

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
    request: Request,
    username=Depends(authenticate_user)
):
    """ Get user by id. """
    logger.info('Get user by id.')

    current_user = await crud.get_user_by_name(request.state.db, username)
    
    # Admin check here
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )
    
    user = await crud.get_user_by_id(request.state.db, user_id)
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
    request: Request,
    user_data: schema.PatchUser,
    username = Depends(authenticate_user)
):
    """ Patch user by id. """
    logger.info('Patch user.')

    current_user = await crud.get_user_by_name(request.state.db, username)
    if not current_user or current_user.id != user_id:
        raise HTTPException(
            status_code=404,
            detail="User not found or invalid permissions.",
        )

    existing_user = await crud.get_user_by_id(request.state.db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    #if user_data.username:
    #    check_username = await crud.get_user_by_name(request.state.db, user_data.username)
    #    if check_username:
    #        raise HTTPException(
    #            status_code=400,
    #            detail="Username already taken",
    #        )
    #    setattr(existing_user, 'username', user_data.username)
    
    if user_data.email:
        check_email = await crud.get_user_by_email(request.state.db, user_data.email)
        if check_email:
            raise HTTPException(
                status_code=400,
                detail="Email already taken",
            )
        setattr(existing_user, 'email', user_data.email)
    
    if user_data.description:
        setattr(existing_user, 'description', user_data.description)

    await request.state.db.commit()
    await request.state.db.refresh(existing_user)
    logger.info('Updated user: %s', existing_user)
    return existing_user


@router.delete(
    path='/{user_id}',
    response_model=schema.ReadUser
)
async def delete_user(
    user_id: int,
    request: Request,
    username=Depends(authenticate_user)
):
    """ Delete a user by id. """
    logger.info('Delete user by id.')

    current_user = await crud.get_user_by_name(request.state.db, username)
    
    # Admin check here
    if not current_user or current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )
    
    deleted_user = await crud.delete_user(request.state.db, user_id)

    logger.info("Deleted user: %s", deleted_user)
    return deleted_user
