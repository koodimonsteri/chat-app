from fastapi import FastAPI, APIRouter

from core.middleware import register_middlewares
from routes import auth
from routes.chat import rest as chat, websocket as chat_ws
from routes.user import rest as user
from routes.admin import admin

app = FastAPI(
    title='Chat application backend',
    debug=True,
    openapi_url='/api/docs',
)


register_middlewares(app)

api_router = APIRouter(
    prefix='/api'
)
ws_router = APIRouter(
    prefix='/ws'
)

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(chat.router)
api_router.include_router(admin.router)

ws_router.include_router(chat_ws.router)

app.include_router(api_router)
app.include_router(ws_router)


@app.get("/")
async def read_root():
    return {"message": "Hello, this is chat-app backend root page!"}
