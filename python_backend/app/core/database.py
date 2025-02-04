import logging
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from core import settings


logger = logging.getLogger('uvicorn')

engine = create_async_engine(
    settings.DB_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


#@asynccontextmanager
#async def get_db():
#    async with AsyncSessionLocal() as session:
#        try:
#            yield session
#        except SQLAlchemyError as e:
#            logger.error('SQLAlchemyError: %s', e)
#            raise e


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error('SQLAlchemyError: %s', e)
            raise e
