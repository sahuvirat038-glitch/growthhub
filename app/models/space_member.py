from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid

class Role(enum.Enum):
    owner = "owner"
    admin = "admin"
    member = "member"

class SpaceMember(Base):
    __tablename__ = 'space_member'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    space_id = Column(UUID(as_uuid=True), ForeignKey('spaces.id'), nullable=False)
    role= Column(Enum(Role), nullable=False, default=Role.member)
    joined_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="memberships")
    space = relationship("Space", back_populates="members")

