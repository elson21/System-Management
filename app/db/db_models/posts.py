from sqlalchemy import(
                    Column, DateTime, ForeignKey, String, Text,
                    func
                )
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..session import Base

class Post(Base):
    __tablename__ = "posts"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Content
    title = Column(String(200))
    content = Column(Text, nullable=False)
    status = Column(String(50))

    # Relationships
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"))
    organization_id = Column(
                        UUID(as_uuid=True),
                        ForeignKey("organizations.id"),
                        nullable=False
                    )
    author_id = Column(
                    UUID(as_uuid=True),
                    ForeignKey("users.id"),
                    nullable=False
                )
    
    # TImestamps
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                )