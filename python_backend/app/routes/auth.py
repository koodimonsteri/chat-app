from datetime import datetime, timezone, timedelta
import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from starlette.requests import Request, HTTPException
from passlib.context import CryptContext

from authentication import load_private_key, load_public_key
from crud import user as crud
from models import User
from schemas import auth as auth_schema, user as user_schema
import settings

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
JWT_PRIVATE_KEY = load_private_key()
JWT_PUBLIC_KEY = load_public_key()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    path='/register',
    description='New users can register in this endpoint.',
    response_model=user_schema.ReadUser
)
async def register(
    user_data: auth_schema.RegisterUser,
    request: Request,
):
    existing_user = await crud.get_user_by_name(request.state.db, user_data.username)
    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    existing_user = await crud.get_user_by_email(request.state.db, user_data.username)
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

    logger.info('Add to db: %s', new_user)
    request.state.db.add(new_user)
    logger.info('Commit')
    await request.state.db.commit()
    logger.info('Refresh')
    await request.state.db.refresh(new_user)
    logger.info('New user: %s', new_user)
    return new_user


@router.post(
    path='/token',
    description='Users can login in this endpoint. Returns JWT Bearer token.',
    response_model=auth_schema.Token
)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    logger.info('Logging in as user: %s', form_data.username)
    existing_user = await crud.get_user_by_name(request.state.db, form_data.username)
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials."
        )
    
    if not pwd_context.verify(form_data.password, existing_user.pw_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials."
        )
    
    payload = {
        "sub": existing_user.username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.JWT_EXPIRES_SECONDS)
    }
    token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)

    return auth_schema.Token(
        token=token,
        token_type="Bearer"
    )

