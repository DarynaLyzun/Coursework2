"""Closet API router.

This module handles the endpoints for managing the user's closet, specifically
uploading clothing items and their associated images.
"""

import shutil
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.routers.auth import get_current_user
from app.database.models import User
from app.crud.item_repo import create_item
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()

UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/closet/upload", response_model=ItemResponse)
async def upload_item(
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Uploads a new clothing item with an image.

    Saves the uploaded image file to the disk and creates a database record
    linking the item to the current user.

    Args:
        file (UploadFile): The image file of the clothing item.
        description (str): A text description (e.g., "Blue denim jacket").
        current_user (User): The authenticated user uploading the item.
        db (Session): Database session.

    Returns:
        Item: The created item record.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, or WebP images are allowed."
        )
    if file.filename:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not save image file."
            )

        item_in = ItemCreate(
            description=description,
            image_filename=unique_filename
        )
    else:
        item_in = ItemCreate(
            description=description
        )
    
    return create_item(db=db, item=item_in, owner_id=current_user.id)