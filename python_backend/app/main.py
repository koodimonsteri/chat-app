from fastapi import FastAPI, APIRouter
from middleware import register_middlewares
from routes import user, auth

app = FastAPI(
    title='Chat application backend'
)

register_middlewares(app)

api_router = APIRouter(
    prefix='/api'
)

api_router.include_router(auth.router)
api_router.include_router(user.router)

app.include_router(api_router)



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Docker!"}