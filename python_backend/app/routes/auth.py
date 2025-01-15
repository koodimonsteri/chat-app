from datetime import datetime, timezone, timedelta

from fastapi import APIRouter
import jwt
from starlette.requests import Request, HTTPException
from passlib.context import CryptContext

from auth import load_private_key, load_public_key
from crud import user as crud
from models import User
from schemas import auth as auth_schema, user as user_schema
import settings

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


JWT_PRIVATE_KEY = load_private_key()
JWT_PUBLIC_KEY = load_public_key()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    path='/register',
    description='New users can register in this endpoint.',
    response_model=user_schema.ReadUser
)
def register(
    user_data: auth_schema.RegisterUser,
    request: Request
):
    existing_user = crud.find_user_by_name(request.state.db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    existing_user = crud.find_user_by_email(request.state.db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        pw_hash=hashed_password
    )

    request.state.db.add(new_user)
    request.state.db.commit()
    request.state.db.refresh(new_user)

    return new_user


@router.post(
    path='/login',
    description='Users can login in this endpoint. Return JWT Bearer token.',
    response_model=auth_schema.Token
)
def login(
    user_data: auth_schema.LoginUser,
    request: Request
):
    existing_user = crud.find_user_by_name(request.state.db, user_data.username)
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials."
        )
    
    if not pwd_context.verify(user_data.password, existing_user.pw_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials."
        )
    
    payload = {
        "sub": existing_user.username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.JWT_EXPIRES_SECONDS)  # Token expires in 30 minutes
    }
    token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)

    return auth_schema.Token(
        token=token,
        token_type="Bearer"
    )

