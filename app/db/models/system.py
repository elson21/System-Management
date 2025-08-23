# app/db/models/system.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class System(Base):
    __tablename__ = "systems"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic ingo
    name = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relationships
    organization_id = Column(
                        UUID(as_uuid=True),
                        ForeignKey("organizations.id"),
                        nullable=False
                    )
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    
    # Notes
    notes = Column(Text(1000))

    # Timestamps
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
    

    def __repr__(self):
        return f"System (id: {self.id}, name: {self.name})"