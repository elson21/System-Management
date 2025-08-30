# app/db/models/system_claims.py

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..session import Base

class SystemClaim(Base):
    __tablename__ = "system_claims"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Notes
    notes = Column(Text)

    # Relationships
    organization_id = Column(
                            UUID(as_uuid=True),
                            ForeignKey("organizations.id"),
                            nullable=False
                        )
    system_id = Column(
                            UUID(as_uuid=True),
                            ForeignKey("systems.id"),
                            nullable=False
                        )
    claimed_by_user_id = Column(
                            UUID(as_uuid=True),
                            ForeignKey("users.id"),
                            nullable=False
                        )
    
    user = relationship("User")
    system = relationship("System")
    
    # Timestamps
    claimed_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                )
    released_at = Column(
                    DateTime(timezone=True),
                    nullable=True   # Null means still claimed
                )