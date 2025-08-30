# app/db/models/system_type.py

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class SystemType(Base):
    __tablename__ = "system_types"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic info
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)

    # Timestamps
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                )