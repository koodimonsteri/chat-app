

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import ChatMessage
from typing import List


async def get_message_history(db: AsyncSession, chat_id: int, start: int = 0, limit: int = 50) -> List[ChatMessage]:
    result = await db.execute(
        select(ChatMessage)
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.asc())
        .offset(start)
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages