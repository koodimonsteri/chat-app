import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt
from starlette.exceptions import HTTPException

import settings

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


def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    logger.info("Authenticating user")
    token = credentials.credentials
    
    decoded = check_jwt(token)
    
    username = decoded.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    logger.info("User authenticated: %s", username)
    return username
