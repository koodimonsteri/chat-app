from cryptography.fernet import Fernet

from core import settings

fernet_context = Fernet(settings.OPENAI_ENCRYPT_KEY.encode())

def encrypt_token(token: str) -> str:
    return fernet_context.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    return fernet_context.decrypt(encrypted_token.encode()).decode()






