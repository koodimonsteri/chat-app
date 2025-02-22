from datetime import datetime

from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict

from schemas import user as user_schema
from core.models import FriendshipStatus



class FriendRequestCreate(BaseModel):
    username: str


class FriendRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    guid: UUID

    sender_id: int
    sender: user_schema.ReadUser
    receiver_id: int
    receiver: user_schema.ReadUser
    
    status: FriendshipStatus

    created_at: datetime


class FriendRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    friend_requests: List[FriendRequest]

