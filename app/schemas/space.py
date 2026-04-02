from pydantic import BaseModel
from uuid import UUID
from datetime import  datetime
from typing import Optional

class SpaceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    member_limit: Optional[int] = 50
    is_public: Optional[bool] = True

class SpaceResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    owner_id: UUID
    member_limit: int
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True