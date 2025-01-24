import logging

from starlette.exceptions import HTTPException
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from exceptions import ResourceNotFoundError
from models import User
from schemas.general import PaginationParams

logger = logging.getLogger('uvicorn')


async def get_all_users(db: AsyncSession, pagination: PaginationParams):
    result = await db.execute(
        select(User)
        #.options(joinedload(User.chats))
        #.options(joinedload(User.friends))
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return result.scalars().all()


async def get_user_by_name(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def create_user(db: AsyncSession, new_user: User):
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    
    if not user:
        raise ResourceNotFoundError("User not found")

    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    return user


