import logging

import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import settings

logger = logging.getLogger('uvicorn')

JWT_PRIVATE_KEY_PATH = f"{settings.JWT_KEYS_DIR}/private.pem"
JWT_PUBLIC_KEY_PATH = f"{settings.JWT_KEYS_DIR}/public.pem"


def load_private_key():
    logger.info('Load private key: %s', JWT_PRIVATE_KEY_PATH)
    with open(JWT_PRIVATE_KEY_PATH, "rb") as key_file:
        return key_file.read()

def load_public_key():
    logger.info('Load public key: %s', JWT_PRIVATE_KEY_PATH)
    with open(JWT_PUBLIC_KEY_PATH, "rb") as key_file:
        return key_file.read()


def create_access_token(data: Dict[str, Any], expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    private_key = load_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> Dict[str, Any]:
    public_key = load_public_key()
    logger.info('public key: %s', public_key)

    try:
        payload = jwt.decode(token, public_key, algorithms=settings.JWT_ALGORITHM)
        logger.info('Payload: %s', payload)
        return payload
    except jwt.PyJWTError:
        raise Exception("Invalid token")
