import os


DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_NAME=os.getenv('DB_NAME')
DB_URL=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DEV=os.getenv('DEV') or 1

JWT_KEYS_DIR=os.getenv('JWT_KEYS_DIR')
JWT_ALGORITHM=os.getenv('JWT_ALGORITHM')
_jwt_expires_seconds = os.getenv('JWT_EXPIRES_SECONDS')
JWT_EXPIRES_SECONDS = int(_jwt_expires_seconds) if _jwt_expires_seconds.isdigit() else 3600

