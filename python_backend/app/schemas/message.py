from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    sender_username: str
    content: str
    # TODO sender_guid

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    sender_id: int
    sender_username: str
    content: str
    created_at: datetime
    updated_at: datetime