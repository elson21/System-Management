# app/db/models/organization.py

from sqlalchemy.orm import Mapped, mapped_column
from ..session import Base

class Organization(Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column