from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class BaseReadUser(BaseModel):

    guid: UUID
    username: str
    email: str
    description: str

    created_at: datetime
    updated_at: datetime


class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    guid: UUID
    username: str
    email: str
    description: str

    created_at: datetime
    updated_at: datetime


class PatchUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    #username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
