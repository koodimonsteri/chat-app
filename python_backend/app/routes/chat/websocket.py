import logging
from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from database import get_db
from models import ChatMessage
from schemas import message as message_schema
from auth import authenticate_user, check_jwt
from crud import user as user_crud

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


chat_connections: Dict[int, List[WebSocket]] = {}



@router.websocket("/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    logger.info('Opening websocket')
    token = websocket.query_params.get("token")
    if not token:
        logger.info('Token missing')
        await websocket.close(code=1008)  # Close connection with "policy violation" code
        return

    try:
        logger.info('Authenticating user.')
        user_id = check_jwt(token)
    except HTTPException as e:
        await websocket.close(code=1008)  # Close connection with "policy violation" code
        return

    username = user_id.get('sub')
    async with get_db() as db:
        current_user = await user_crud.get_user_by_name(db, username)

    if not current_user:
        raise HTTPException(404, 'User not found')
    
    logger.info('New user connected: %s', username)
    await websocket.accept()

    if chat_id not in chat_connections:
        chat_connections[chat_id] = []
    chat_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            logger.info('Received data: %s', data)
            message_data = message_schema.MessageCreate(**data)

            async with get_db() as db:
                try:
                    message = ChatMessage(
                        chat_id=chat_id,
                        sender_id=current_user.id,
                        sender_username=current_user.username,
                        content=message_data.content,
                    )
                    db.add(message)
                    await db.commit()
                    await db.refresh(message)
                    logger.info('Created message: %s', message)
                    broadcast_message = message_schema.MessageRead.model_validate(message)
                except SQLAlchemyError as e:
                    logger.error('Database error..')
                    logger.exception(e)
                    await websocket.send_json({"error": "Database error occurred."})
                    continue
            temp = broadcast_message.model_dump(mode='json')
            logger.info('Serialized message: %s', temp)
            for conn in chat_connections[chat_id]:
                #if conn != websocket:
                await conn.send_json(temp)

    except WebSocketDisconnect:
        chat_connections[chat_id].remove(websocket)
        if not chat_connections[chat_id]:
            del chat_connections[chat_id]

