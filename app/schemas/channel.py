from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    space_id: UUID

class ChannelResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    space_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True