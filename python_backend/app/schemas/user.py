from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

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


class PatchUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    #username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None


