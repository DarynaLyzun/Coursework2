"""Database connection and session management.

This module handles the connection to the MariaDB database using SQLAlchemy.
It configures the connection pool settings to ensure stability and provides
a dependency callable for FastAPI to manage database sessions per request.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Creates a new database session for a single request.

    This function is designed to be used as a FastAPI dependency. It ensures
    that a database session is created before the request is processed and
    closed immediately after, even if an exception occurs during the request.

    Yields:
        Session: A standard SQLAlchemy session object connected to the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()