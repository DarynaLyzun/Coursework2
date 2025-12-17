"""Integration tests for closet management endpoints."""

import io
from unittest.mock import MagicMock, mock_open, patch

from fastapi.testclient import TestClient

from app.database.models import Item, User
from app.database.session import get_db
from app.routers.auth import get_current_user
from main import app


def setup_app(db_session, mock_user, mock_ai_service=None):
    """Configures the app with database, user, and AI service mocks.

    Args:
        db_session: The database session fixture.
        mock_user: The mock user instance.
        mock_ai_service: The mock AI service instance (optional).

    Returns:
        TestClient: Configured test client.
    """
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: mock_user

    if mock_ai_service:
        app.state.ai_service = mock_ai_service

    return TestClient(app)


def test_upload_item_success(db_session):
    """Verifies successful item upload and AI classification.

    Args:
        db_session: The database session fixture.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")

    mock_ai = MagicMock()
    mock_ai.classify.return_value = {
        "labels": ["Cold", "Rain"],
        "scores": [0.99, 0.10],
    }

    with patch("pathlib.Path.open", mock_open()) as mocked_file, patch(
        "app.routers.closet.shutil.copyfileobj"
    ) as mock_copy:

        client = setup_app(db_session, mock_user, mock_ai)

        file_content = b"fake_image_bytes"
        files = {
            "file": ("test_image.jpg", io.BytesIO(file_content), "image/jpeg")
        }
        data = {"description": "Thick winter coat"}

        response = client.post("/closet/upload", files=files, data=data)

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["description"] == "Thick winter coat"
        assert json_data["owner_id"] == 1


def test_upload_invalid_file_type(db_session):
    """Verifies that uploading invalid file types returns an error.

    Args:
        db_session: The database session fixture.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    client = setup_app(db_session, mock_user)

    files = {"file": ("notes.txt", io.BytesIO(b"text content"), "text/plain")}
    data = {"description": "Wrong file type"}

    response = client.post("/closet/upload", files=files, data=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid image type."


def test_get_closet_items(db_session):
    """Verifies retrieval of items from the closet.

    Args:
        db_session: The database session fixture.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    db_session.add(mock_user)
    
    # Add items directly to DB
    item1 = Item(description="Item 1", image_filename="1.jpg", owner_id=1)
    item2 = Item(description="Item 2", image_filename="2.jpg", owner_id=1)
    db_session.add_all([item1, item2])
    db_session.commit()

    client = setup_app(db_session, mock_user)
    response = client.get("/closet")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Item 1"


def test_delete_item_success(db_session):
    """Verifies that an item can be deleted via the API.

    Args:
        db_session: The database session fixture.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    db_session.add(mock_user)
    
    item = Item(description="Delete Me", image_filename="del.jpg", owner_id=1)
    db_session.add(item)
    db_session.commit()
    item_id = item.id

    client = setup_app(db_session, mock_user)

    # Mock os.remove to avoid filesystem errors
    with patch("os.remove") as mock_remove:
        with patch("pathlib.Path.exists", return_value=True):
            response = client.delete(f"/closet/{item_id}")
    
    assert response.status_code == 204
    
    # Check DB
    assert db_session.query(Item).filter_by(id=item_id).first() is None


def test_delete_item_not_found(db_session):
    """Verifies 404 error when deleting a non-existent item.

    Args:
        db_session: The database session fixture.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    client = setup_app(db_session, mock_user)

    response = client.delete("/closet/9999")
    assert response.status_code == 404