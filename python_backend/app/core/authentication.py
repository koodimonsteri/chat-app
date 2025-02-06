import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user
from core.database import get_db
from core.models import User, UserRole
from core import settings

logger = logging.getLogger('uvicorn')

JWT_PRIVATE_KEY_PATH = f"{settings.JWT_KEYS_DIR}/private.pem"
JWT_PUBLIC_KEY_PATH = f"{settings.JWT_KEYS_DIR}/public.pem"

security = HTTPBearer() 

def load_private_key():
    logger.info('Load private key: %s', JWT_PRIVATE_KEY_PATH)
    with open(JWT_PRIVATE_KEY_PATH, "rb") as key_file:
        return key_file.read()

def load_public_key():
    logger.info('Load public key: %s', JWT_PRIVATE_KEY_PATH)
    with open(JWT_PUBLIC_KEY_PATH, "rb") as key_file:
        return key_file.read()


def create_jwt(data: Dict[str, Any], expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    private_key = load_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def check_jwt(token: str) -> Dict[str, Any]:
    public_key = load_public_key()

    try:
        payload = jwt.decode(token, public_key, algorithms=settings.JWT_ALGORITHM)
        logger.info('Payload: %s', payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


async def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_db)
) -> User:
    logger.info("Authenticating user")
    token = credentials.credentials

    decoded = check_jwt(token)
    
    username = decoded.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    current_user = await user.get_user_by_name(db_session, username)

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    logger.info("User authenticated: %s", username)
    
    return current_user


async def admin_required(
    current_user: User = Depends(authenticate_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="You do not have the required permissions"
        )
    return current_user