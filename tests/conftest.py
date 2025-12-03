"""Pytest configuration and fixtures.

This module defines shared fixtures for the testing suite, specifically
handling the in-memory SQLite database connection to ensure tests run
in isolation without affecting the local MariaDB instance.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh, isolated database session for a single test.

    This fixture creates all tables in the in-memory SQLite database before
    the test runs and drops them immediately after. This ensures that data
    from one test does not leak into another.

    Yields:
        Session: A SQLAlchemy session connected to the in-memory database.
    """
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)