from models import User
from sqlalchemy.orm import Session


def find_user_by_name(db: Session, username: str):
    existing_user = db.query(User).filter(
        User.username == username).one_or_none()
    return existing_user


def find_user_by_email(db: Session, email: str):
    existing_user = db.query(User).filter(
        User.email == email).one_or_none()
    return existing_user


