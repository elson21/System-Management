# app/db/session.py

"""
Database configuration and setup module.

This module configures the SQLAlchemy for the System Management application.
It provides:
    - Database engine
    - Session factory for creating database sessions
    - Base class for all ORM models
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# read the .env
load_dotenv()

# Parent class for all models
class Base(DeclarativeBase):
    pass

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found...")

engine = create_engine(
    DATABASE_URL,
    echo=True,          # print SQL to see what's hapening
    pool_pre_ping=True  # check if connection is live
)

# Session factory - create new db sessions
SessionLocal = sessionmaker(bind=engine)