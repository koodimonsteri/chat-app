import logging
from typing import List

from fastapi import FastAPI, Request#, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from jose import jwt
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware

from authentication import load_public_key
from database import get_db
#from crud import user as user_crud
import settings


logger = logging.getLogger("uvicorn")


def register_cors(app: FastAPI):
    origins = [
        'http://localhost:3000',
        '*'
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*']
    )


def register_exception_handlers(app: FastAPI):
    # database exceptions
    logger.info('Register sqlalchemy exception handler.')
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
        logger.error(f"SQLAlchemyError: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "A database error occurred. Please try again later."},
        )

    # http exceptions
    logger.info('Register http exception handler.')
    @app.exception_handler(StarletteHTTPException)
    async def my_exception_handler(request, exc: StarletteHTTPException):
        logger.info('On starlette HTTPException handler')
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )
    app.add_exception_handler(StarletteHTTPException, my_exception_handler)

    # fallback exception handler
    logger.info('Register unhandled exception handler.')
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        logger.error('On general exception handler')
        if isinstance(exc, StarletteHTTPException):
            logger.error('This is starlette exception!!')
        logger.error(f"Unexpected error: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred. Please try again later."},
        )


def register_db_session(app: FastAPI): 
    class AsyncDBSessionMiddleware(BaseHTTPMiddleware):
        def __init__(self, app):
            super().__init__(app)

        async def dispatch(self, request: Request, call_next):
            logger.info("DB session middleware start")

            async with get_db() as db:
                request.state.db = db
                
                try:
                    response = await call_next(request)
                    logger.debug("Async DB session middleware completed call_next")
                    await db.commit()
                except Exception as e:
                    await db.rollback()
                    raise e
                finally:
                    await db.close()
                    logger.info("Async DB session middleware end")
            return response
        
    app.add_middleware(AsyncDBSessionMiddleware)


JWT_PUBLIC_KEY = load_public_key()

def register_authentication(app: FastAPI, exclude_paths: List[str]):

    class AuthenticationMiddleware(BaseHTTPMiddleware):
        
        def __init__(self, app: FastAPI, exclude_paths: List[str]):
            super().__init__(app)
            self.exclude_paths = exclude_paths

        async def dispatch(self, request: Request, call_next):
            logger.info("Authentication middleware start")
            if request.method == "OPTIONS":
                response = await call_next(request)
                return response

            if any(request.url.path.startswith(path) for path in self.exclude_paths):
                return await call_next(request)

            auth_header = request.headers.get("Authorization")
            logger.info('Auth header: %s', auth_header)
            if not auth_header or not auth_header.startswith("Bearer "):
                raise StarletteHTTPException(status_code=401, detail="Missing or invalid Authorization header")

            token = auth_header.split(" ")[1]
            try:
                decoded = jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise StarletteHTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise StarletteHTTPException(status_code=401, detail="Invalid token")
            request.state.username = decoded.get('sub')
            logger.info("Authentication middleware end")
            return await call_next(request)

    app.add_middleware(AuthenticationMiddleware, exclude_paths=exclude_paths)


def register_middlewares(app: FastAPI):

    logger.info('Register exception handlers.')
    register_exception_handlers(app)

    logger.info('Register cors middleware.')
    register_cors(app)

    logger.info('Register authentication middleware.')
    exclude_paths = ['/api/auth/token', '/api/auth/register', '/api/docs', '/docs']
    #register_authentication(app, exclude_paths)

    logger.info('Register db session middleware.')
    register_db_session(app)
