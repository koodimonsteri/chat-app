from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field

from core.models import ChatBotType
from core.openai import decrypt_token


class BaseReadChatBot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class ReadChatBot(BaseReadChatBot):

    type: ChatBotType
    system_prompt: str
    api_token: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    @field_validator("api_token", mode="before")
    @classmethod
    def decrypt_openai_token(cls, v):
        if v:
            try:
                return decrypt_token(v)
            except Exception as e:
                return ''
        return v


class CreateChatBot(BaseModel):

    name: str = Field(..., min_length=4, max_length=255)
    system_prompt: Optional[str]
    api_token: Optional[str]
    chatbot_type: ChatBotType

