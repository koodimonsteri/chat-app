import logging

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


logger = logging.getLogger('uvicorn')


async def get_user_by_name(db: AsyncSession, username: str):
    """Fetch a user by username asynchronously."""
    logger.info("Querying user by name: %s", username)

    query = select(User).where(User.username == username)
    result = await db.execute(query)

    existing_user = result.scalars().one_or_none()
    logger.info("Result: %s", existing_user)
    return existing_user


async def get_user_by_email(db: AsyncSession, email: str):
    """Fetch a user by email asynchronously."""
    logger.info("Querying user by email: %s", email)

    query = select(User).where(User.email == email)
    result = await db.execute(query)

    existing_user = result.scalars().one_or_none()
    logger.info("Result: %s", existing_user)
    return existing_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Fetch a user by ID asynchronously."""
    logger.info("Querying user by id: %s", user_id)

    query = select(User).where(User.id == user_id)
    result = await db.execute(query)

    existing_user = result.scalars().one_or_none()
    logger.info("Result: %s", existing_user)
    return existing_user
