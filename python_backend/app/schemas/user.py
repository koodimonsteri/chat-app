from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from core.openai import decrypt_token


class BaseReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guid: UUID
    username: str
    description: str

    created_at: datetime
    updated_at: datetime


class ReadUser(BaseReadUser):

    id: int
    email: str
    openai_token: str

    @field_validator("openai_token", mode="before")
    @classmethod
    def decrypt_openai_token(cls, v):
        if v:
            try:
                return decrypt_token(v)
            except Exception as e:
                return ''
        return v


class PatchUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    #username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    openai_token: Optional[str] = None

    