# app/db/models/department_membership.py

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class DepartmentMembership(Base):
    __tablename__ = "department_memberships"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relationships
    user_id = Column(
                UUID(as_uuid=True),
                ForeignKey("users.id"),
                nullable=False
            )
    department_id = Column(
                UUID(as_uuid=True),
                ForeignKey("departments.id"),
                nullable=False
            )
    organization_id = Column(
                UUID(as_uuid=True),
                ForeignKey("organizations.id"),
                nullable=False
            )
    
    # Role of the user in a department ("lead", "guest", "tester", etc)
    role = Column(String(20), nullable=False)

    # Timestamps
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False)