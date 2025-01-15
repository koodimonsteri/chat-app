import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal


logger = logging.getLogger("uvicorn")


def register_cors(app: FastAPI):
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # List of origins you want to allow
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods, can be restricted
        allow_headers=["*"],  # Allows all headers, can be restricted
    )


def register_exception_handlers(app: FastAPI):
    # Not really middleware, but close enough

    # database exceptions
    logger.info('Register sqlalchemy exception handler.')
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request, exc):
        logger.error(f"SQLAlchemyError: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "A database error occurred. Please try again later."},
        )

    # http exceptions
    logger.info('Register http excetion handler.')
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    # fallback exception handler
    logger.info('Register unhandled exception handler.')
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unexpected error: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred. Please try again later."},
        )


def registed_db_session(app: FastAPI):
    class DBSessionMiddleware(BaseHTTPMiddleware):
        def __init__(self, app):
            super().__init__(app)

        async def dispatch(self, request: Request, call_next):
            db = SessionLocal()
            request.state.db = db
            try:
                response = await call_next(request)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
            return response
        
    app.add_middleware(DBSessionMiddleware)


def register_middlewares(app: FastAPI):

    logger.info('Register exception handlers.')
    register_exception_handlers(app)

    logger.info('Register cors middleware.')
    register_cors(app)

    logger.info('Register db session middleware.')
    registed_db_session(app)
