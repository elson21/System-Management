# app/db/models/organization.py

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class Organization(Base):
    __tablename__ = "organizations"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic info
    name = Column(String(200), unique=True, nullable=False, index=True)
    created_at = Column(
                DateTime(timezone=True),
                server_default=func.now(),
                nullable=False
            )