from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    space_id = Column(UUID(as_uuid=True), ForeignKey('spaces.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    space = relationship("Space", back_populates="channels")
    messages = relationship("Message", back_populates="channel")