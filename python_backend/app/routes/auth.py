from datetime import datetime, timezone, timedelta
import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from starlette.requests import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from core.authentication import load_private_key, load_public_key
from core.database import get_db
from crud import user as crud
from core.models import User
from schemas import auth as auth_schema, user as user_schema
from core import settings

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
    db_session: AsyncSession = Depends(get_db)
):
    existing_user = await crud.get_user_by_name(db_session, user_data.username)
    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    existing_user = await crud.get_user_by_email(db_session, user_data.username)
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

    created = await crud.create_user(db_session, new_user)
    return created


@router.post(
    path='/token',
    description='Users can login in this endpoint. Returns JWT Bearer token.',
    response_model=auth_schema.Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db)
):
    logger.info('Logging in as user: %s', form_data.username)
    existing_user = await crud.get_user_by_name(db_session, form_data.username)
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
        "role": existing_user.role.value,
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.JWT_EXPIRES_SECONDS)
    }
    token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)

    return auth_schema.Token(
        token=token,
        token_type="Bearer"
    )

