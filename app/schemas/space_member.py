from pydantic import BaseModel
from uuid import UUID
from datetime import  datetime

class SpaceMemberResponse(BaseModel):
    id: UUID
    user_id: UUID
    space_id: UUID
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True