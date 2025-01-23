import logging
from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from database import get_db
from models import ChatMessage
from schemas import message as msg_schema
from authentication import check_jwt
from crud import user as user_crud, message as msg_crud, chat as chat_crud

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


chat_connections: Dict[int, Dict[int, WebSocket]] = {}

#https://github.com/Luka967/websocket-close-codes


@router.websocket("/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    logger.info('Opening websocket')
    token = websocket.query_params.get("token")
    if not token:
        logger.info('Token missing')
        await websocket.close(code=3000)
        return

    try:
        logger.info('Authenticating user.')
        token_data = check_jwt(token)
    except HTTPException as e:
        logger.error('Invalid JWT')
        await websocket.close(code=3000)
        return

    username = token_data.get('sub')

    try:
        async with get_db() as db:

            current_user = await user_crud.get_user_by_name(db, username)
            if not current_user:
                logger.error('Failed to get user: %s', username)
                await websocket.close(code=3000)
                return
            logger.info('Current user: %s', current_user)

            chat = await chat_crud.get_chat_by_id(db, chat_id)
            if not chat:
                logger.error('Failed to get chat: %s', chat_id)
                await websocket.close(code=3000)
                return
            logger.info('Current chat: %s', chat)

            if current_user not in chat.users:
                logger.info('Adding user to chat.')
                chat.users.append(current_user)
                db.add(chat)
                await db.commit()
                await db.refresh(chat)

                
    except SQLAlchemyError as e:
        logger.error('Error while joining chat..')
        logger.exception(e)
        await websocket.close(code=3001)
        return
    
    await websocket.accept()
    logger.info('New user connected: %s', username)

    if chat_id not in chat_connections:
        chat_connections[chat_id] = {}
    chat_connections[chat_id][current_user.id] = websocket

    try:
        async with get_db() as db:

            messages = await msg_crud.get_message_history(db, chat_id)
            logger.info('Messages: %s', messages)

            for msg in messages:
                logger.info('New msg: %s', msg)
                message = msg_schema.MessageRead.model_validate(msg)
                logger.info('New message: %s', message)
                await websocket.send_json(message.model_dump(mode='json'))

    except SQLAlchemyError as e:
        logger.error('Error fetching message history')
        logger.exception(e)
        await websocket.send_json({"error": "Error fetching message history."})
        await websocket.close(code=3001)
        return

    try:
        while True:
            data = await websocket.receive_json()
            logger.info('Received data: %s', data)
            message_data = msg_schema.MessageCreate.model_validate(data)

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
                except SQLAlchemyError as e:
                    logger.error('Database error..')
                    logger.exception(e)
                    await websocket.send_json({"error": "Database error occurred."})
                    continue
            
                try:
                    logger.info('Before validate: %s', message)
                    broadcast_message = msg_schema.MessageRead.model_validate(message)
                    logger.info('After validate: %s', message)
                    msg = broadcast_message.model_dump(mode='json')
                    logger.info('Serialized message: %s', msg)
                    logger.info('len chat connections: %s', len(chat_connections[chat_id]))
                    for user_id, ws in chat_connections[chat_id].items():
                        #if conn != websocket:
                        logger.info('Broadcasting to: %s', user_id)
                        await ws.send_json(msg)

                except Exception as e:
                    logger.error('Failed to broadcast message.')
                    logger.exception(e)
                    continue

    except WebSocketDisconnect:
        del chat_connections[chat_id][current_user.id]
        if not chat_connections[chat_id]:
            del chat_connections[chat_id]

