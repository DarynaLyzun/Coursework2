"""Unit tests for session management."""

from unittest.mock import MagicMock, patch

from app.database.session import get_db


def test_get_db_lifecycle():
    """Verifies session lifecycle management in dependency."""
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
    """Verifies session closure upon error."""
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