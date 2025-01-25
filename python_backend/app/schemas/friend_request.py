from uuid import UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

class FriendshipStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class FriendRequestCreate(BaseModel):
    username: str


class FriendRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guid: UUID
    sender_id: int
    receiver_id: int
    status: FriendshipStatus
    created_at: datetime

