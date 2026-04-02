from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid


class AuthProvider(enum.Enum):
    email    = "email"
    google   = "google"
    github = "github"

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    provider = Column(Enum(AuthProvider), nullable=False, default=AuthProvider.email)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    memberships = relationship("SpaceMember", back_populates="user")
    messages = relationship("Message", back_populates="author")
    owned_spaces = relationship("Space", back_populates="owner")