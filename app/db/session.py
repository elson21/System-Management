# app/db/session.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# read the .env
load_dotenv()

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found...")

engine = create_engine(   
    "DATABASE_URL",
    echo=True,          # print SQL to see what's hapening
    pool_pre_ping=True  # check if connection is live
)

session = sessionmaker(engine)