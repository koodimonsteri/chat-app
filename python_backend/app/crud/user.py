import logging
from models import User
from sqlalchemy.orm import Session

logger = logging.getLogger('uvicorn')

def get_user_by_name(db: Session, username: str):
    logger.info('Querying user by name: %s', username)
    existing_user = db.query(User).filter(
        User.username == username).one_or_none()
    logger.info('Result: %s', existing_user)
    return existing_user


def get_user_by_email(db: Session, email: str):
    logger.info('Querying user by email: %s', email)
    existing_user = db.query(User).filter(
        User.email == email).one_or_none()
    logger.info('Result: %s', existing_user)
    return existing_user


def get_user_by_id(db: Session, user_id: int):
    logger.info('Querying user by id: %s', user_id)
    existing_user = db.query(User).filter(
        User.id == user_id).one_or_none()
    logger.info('Result: %s', existing_user)
    return existing_user

