import logging

from fastapi import APIRouter, Depends

from core.authentication import admin_required
from routes.admin.user import router as user_router

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/admin',
    tags=["admin"],
    dependencies=[Depends(admin_required)]
)

router.include_router(user_router)


@router.get('')
async def check_admin():
    return {'message': 'Wiiiii admin stuff here :)'}