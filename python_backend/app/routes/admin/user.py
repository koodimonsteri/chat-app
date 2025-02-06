import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.authentication import authenticate_user
from core.database import get_db
from core.models import User
from schemas import user as user_schema

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/user'


)



#@router.get(
#    path='/{user_id}',
#    response_model=user_schema.ReadUser
#)
#async def get_user_by_id(
#    user_id: int,
#    current_user: User = Depends(authenticate_user),
#    db_session: AsyncSession = Depends(get_db)
#):
#    """ Get user by id. """
#    logger.info('Get user by id.')
#
#    #current_user = await crud.get_user_by_name(request.state.db, username)
#    
#    # Admin check here
#    if current_user.id != user_id:
#        raise HTTPException(
#            status_code=403,
#            detail="Insufficient permissions",
#        )
#    
#    user = await crud.get_user_by_id(db_session, user_id)
#    if not user:
#        raise HTTPException(
#                status_code=403,
#                detail="User not found",
#            )
#
#    return user