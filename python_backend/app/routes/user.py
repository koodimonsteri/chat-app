import logging

from fastapi import APIRouter
from starlette.requests import Request
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

import jwt
import settings
from schemas import user as schema
from crud import user as crud 

logger = logging.getLogger('uvicorn')


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get(
    path='/me',
    response_model=schema.ReadUser
)
async def get_me(request: Request):
    """ Get current user. """
    user = await crud.get_user_by_name(request.state.db, request.state.username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user

    

@router.patch(
    path='/{user_id}',
    response_model=schema.ReadUser
)
async def patch_user(
    user_id: int,
    request: Request,
    user_data:  schema.PatchUser
):
    """ Patch user by id. """
    # TODO patch only self or with admin rights.
    logger.info('Patch user.')
    existing_user = await crud.get_user_by_id(request.state.db, user_id)

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user_data.username:
        check_username = await crud.get_user_by_name(request.state.db, user_data.username)
        if not check_username:
            raise HTTPException(
                status_code=400,
                detail="Username already taken",
            )
        setattr(existing_user, 'username', user_data.username)
    
    if user_data.email:
        check_email = await crud.get_user_by_email(request.state.db, user_data.email)
        if not check_email:
            raise HTTPException(
                status_code=400,
                detail="Email already taken",
            )
        setattr(existing_user, 'email', user_data.email)
    
    if user_data.description:
        setattr(existing_user, 'description', user_data.description)

    logger.info("Committing changes to the user.")
    await request.state.db.commit()
    logger.info("Refreshing the updated user.")
    await request.state.db.refresh(existing_user)

    logger.info("Returning updated user: %s", existing_user)
    return existing_user
