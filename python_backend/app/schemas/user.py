from pydantic import BaseModel
from datetime import datetime



class ReadUser(BaseModel):

    username: str
    email: str
    description: str
    created_at: datetime
    updated_at: datetime