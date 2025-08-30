# app/db/models/department.py

from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class Department(Base):
    __tablename__ = "departments"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic info
    name = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    organization_id = Column(
                        UUID(as_uuid=True),
                        ForeignKey("organizations.id"),
                        nullable=False
                    )

    # Timestamps
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                    )
    

    def __repr__(self):
        return f"Department(id: {self.id}, name: {self.name})"