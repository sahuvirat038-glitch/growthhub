from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    channel_id: UUID
    expires_at: Optional[datetime] = None

class MessageResponse(BaseModel):
    id: UUID
    content: str
    channel_id: UUID
    author_id: UUID
    author_email : Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True