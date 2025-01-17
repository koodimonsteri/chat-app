
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from schemas import user as user_schema


class GetChatsParams(BaseModel):
    start: int = Field(0, ge=0, description="Start index for pagination")
    limit: int = Field(100, gt=0, le=100, description="Maximum number of chats to return")
    chat_name: Optional[str] = Field(None, description="Filter chats by name. Case-insesitive search")
    current_user: bool = Field(False, description='Fetch current user chats if true.')


class ReadChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

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
