
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from schemas import user as user_schema
from schemas.general import PaginationParams

class GetChatsParams(PaginationParams):
    chat_name: Optional[str] = Field(None, description="Filter chats by name. Case-insesitive search")
    current_user: bool = Field(False, description='Fetch current user chats if true.')


class ChatOwnerResponse(BaseModel):
    guid: UUID
    username: str
    

# Todo separate basechat
class ReadChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    guid: UUID

    name: str
    description: str
    is_private: bool
    chat_owner: user_schema.ReadUser

    created_at: datetime
    updated_at: datetime
    
    users: List[user_schema.ReadUser]


class CreateChat(BaseModel):
    name: str = Field(..., min_length=4, max_length=255, description='Name of the chat.')
    description: str = Field('', description='Free text description for chat.')
    is_private: bool = Field(False, description='Private or public chat')
