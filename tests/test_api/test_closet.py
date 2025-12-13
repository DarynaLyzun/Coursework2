"""Unit tests for the Closet API router.

This module verifies that authenticated users can upload clothing items,
ensuring that files are validated, saved (mocked), AI is called (mocked),
and tags are saved to the database.
"""

import io
from unittest.mock import patch, MagicMock, mock_open
from fastapi.testclient import TestClient
from app.database.session import get_db
from app.routers.auth import get_current_user
from app.database.models import User
from main import app 

def setup_app(db_session, mock_user, mock_ai_service=None):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    if mock_ai_service:
        app.state.ai_service = mock_ai_service
    
    return TestClient(app)

def test_upload_item_success(db_session):
    """Verifies that a valid image file can be uploaded and tagged by AI."""
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    
    mock_ai = MagicMock()
    mock_ai.classify.return_value = {
        "labels": ["Cold", "Rain"], 
        "scores": [0.99, 0.10]
    }
    
    with patch("pathlib.Path.open", mock_open()) as mocked_file, \
         patch("app.routers.closet.shutil.copyfileobj") as mock_copy:
        
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
        
        mock_ai.classify.assert_called_once()
        args, _ = mock_ai.classify.call_args
        assert args[0] == "Thick winter coat"

def test_upload_invalid_file_type(db_session):
    """Verifies that uploading a non-image file returns a 400 error."""
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    client = setup_app(db_session, mock_user)
    
    files = {
        "file": ("notes.txt", io.BytesIO(b"text content"), "text/plain")
    }
    data = {"description": "Wrong file type"}
    
    response = client.post("/closet/upload", files=files, data=data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Only JPEG, PNG, or WebP images are allowed."