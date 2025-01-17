from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



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

    username: str = None
    email: str = None
    description: str = None