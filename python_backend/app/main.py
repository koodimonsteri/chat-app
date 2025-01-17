from fastapi import FastAPI, APIRouter
from middleware import register_middlewares
from routes import user, auth, chat

app = FastAPI(
    title='Chat application backend',
    debug=True,
    openapi_url='/api/docs'
)

register_middlewares(app)

api_router = APIRouter(
    prefix='/api'
)

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(chat.router)

app.include_router(api_router)



@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with Docker!"}