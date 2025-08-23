# app/db/models/user.py

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from ..session import Base

class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic info
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100),unique=True, nullable=False, index=True)

    # Password has
    password_hash = Column(String(255))

    # Relationships
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))

    # Status and optional fields
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    last_login = Column(DateTime(timezone=True),)
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                    )
    updated_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    onupdate=func.now(),
                    nullable=True
                    )
    email_verified_at = Column(
                    DateTime(timezone=True),
                    nullable=True
                    )