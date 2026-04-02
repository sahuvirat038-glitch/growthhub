from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Space(Base):
    __tablename__ = "spaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    member_limit = Column(Integer, default=50)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User", back_populates="owned_spaces")
    members = relationship("SpaceMember", back_populates="space")
    channels = relationship("Channel", back_populates="space")