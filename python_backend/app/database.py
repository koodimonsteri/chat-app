import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
import settings


logger = logging.getLogger('uvicorn')

engine = create_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
    
    except SQLAlchemyError as e:
        logger.error('SQLAlchemyError: %s', e)
        raise e
    except Exception as e:
        logger.error('SessionLocal failed :()')
    return db