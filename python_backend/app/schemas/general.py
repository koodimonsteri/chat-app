from pydantic import BaseModel, Field


class PaginationParams(BaseModel):

    start: int = Field(0, ge=0, description="Start index for pagination")
    limit: int = Field(100, gt=0, le=100, description="Maximum number of chats to return")