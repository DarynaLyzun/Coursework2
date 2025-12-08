"""Unit tests for the Closet API router.

This module verifies that authenticated users can upload clothing items,
ensuring that files are validated, saved (mocked), and recorded in the database.
"""

import io
from unittest.mock import patch, MagicMock, mock_open
from fastapi.testclient import TestClient
from app.database.session import get_db
from app.routers.auth import get_current_user
from app.database.models import User
from main import app 

def setup_app(db_session, mock_user):
    app.dependency_overrides[get_db] = lambda: db_session
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    return TestClient(app)

def test_upload_item_success(db_session):
    """Verifies that a valid image file can be uploaded.
    
    Ensures that:
    1. The file is accepted.
    2. The image is 'saved' (mocked).
    3. The database record is created with the correct owner.
    """
    mock_user = User(id=1, email="test@owner.com", hashed_password="pw")
    
    with patch("pathlib.Path.open", mock_open()) as mocked_file, \
         patch("app.routers.closet.shutil.copyfileobj") as mock_copy:
        
        client = setup_app(db_session, mock_user)
        
        file_content = b"fake_image_bytes"
        files = {
            "file": ("test_image.jpg", io.BytesIO(file_content), "image/jpeg")
        }
        data = {"description": "My cool jacket"}
        
        response = client.post("/closet/upload", files=files, data=data)
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["description"] == "My cool jacket"
        assert json_data["owner_id"] == 1
        assert "image_filename" in json_data
        
        mocked_file.assert_called()
        mock_copy.assert_called()

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