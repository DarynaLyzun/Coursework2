"""Unit tests for database session management.

This module verifies that the database session lifecycle is managed correctly,
ensuring sessions are closed after use, even when mocked.
"""

from unittest.mock import MagicMock, patch
from app.database.session import get_db

def test_get_db_lifecycle():
    """Verifies that get_db opens and closes the session correctly.

    Mocks the SessionLocal class to avoid creating a real DB connection,
    then iterates through the generator to ensure the session is yielded
    and subsequently closed, verifying the context manager behavior.
    """
    mock_session = MagicMock()

    with patch("app.database.session.SessionLocal", return_value=mock_session):
        generator = get_db()
        yielded_session = next(generator)
        
        assert yielded_session == mock_session

        try:
            next(generator)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()
        
def test_get_db_closes_on_error():
    """Verifies that the session closes even if an error occurs during usage.

    Simulates an exception occurring while the session is in use to ensure
    that the cleanup logic (db.close) is still executed in the finally block.
    """
    mock_session = MagicMock()
    
    with patch("app.database.session.SessionLocal", return_value=mock_session):
        generator = get_db()
        next(generator)

        try:
            generator.throw(ValueError)
            pass 
        except ValueError:
            pass

        mock_session.close.assert_called_once()