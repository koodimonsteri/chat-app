from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    username: str
    email: str
    description: str

    created_at: datetime
    updated_at: datetime


class PatchUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None