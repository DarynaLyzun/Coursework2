"""API endpoints for managing the user's closet."""

import os
import shutil
import uuid
from pathlib import Path
from typing import Annotated, Any, List

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.utils import CANDIDATE_LABELS, INCOMPATIBLE_KEYWORDS
from app.crud.item_repo import create_item
from app.crud.tag_repo import get_or_create_tag, link_item_to_tag
from app.database.models import ClothingWeather, Item, User
from app.database.session import get_db
from app.routers.auth import get_current_user
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()
UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def item_to_response(item: Any) -> dict:
    """Helper to convert an Item model to a response dictionary.

    Args:
        item (Any): The Item model instance.

    Returns:
        dict: The serialized item data.
    """
    tags = []
    if hasattr(item, "weather_links"):
        tags = [link.tag.name for link in item.weather_links if link.tag]

    return {
        "id": item.id,
        "owner_id": item.owner_id,
        "description": item.description,
        "image_filename": item.image_filename,
        "tags": tags,
    }


@router.post("/closet/upload", response_model=ItemResponse)
async def upload_item(
    request: Request,
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Uploads a new clothing item, saves the image, and processes tags via AI.

    Args:
        request (Request): The request object containing application state.
        file (UploadFile): The uploaded image file.
        description (str): A description of the clothing item.
        current_user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        ItemResponse: The created item with generated tags.

    Raises:
        HTTPException: If the file type is invalid or saving fails.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid image type.")

    file_extension = (
        file.filename.split(".")[-1]
        if file.filename and "." in file.filename
        else "jpg"
    )
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save file.")

    item_in = ItemCreate(description=description, image_filename=unique_filename)
    new_item = create_item(db=db, item=item_in, owner_id=current_user.id)

    ai_service = request.app.state.ai_service
    if ai_service:
        results = ai_service.classify_description(
            text=description,
            candidate_labels=CANDIDATE_LABELS,
            hypothesis_template="This item is worn when the weather is {}.",
        )

        for label, score in results.items():
            if label in INCOMPATIBLE_KEYWORDS:
                if any(
                    k in description.lower() for k in INCOMPATIBLE_KEYWORDS[label]
                ):
                    continue

            if score > 70:
                tag = get_or_create_tag(db, label)
                link_item_to_tag(db, new_item.id, tag.id, score)

    db.refresh(new_item)
    return item_to_response(new_item)


@router.get("/closet", response_model=List[ItemResponse])
def get_closet(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Retrieves all items in the authenticated user's closet.

    Args:
        current_user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        List[ItemResponse]: A list of clothing items.
    """
    stmt = (
        select(Item)
        .where(Item.owner_id == current_user.id)
        .options(joinedload(Item.weather_links).joinedload(ClothingWeather.tag))
    )
    items = db.scalars(stmt).unique().all()

    return [item_to_response(item) for item in items]


@router.delete("/closet/{item_id}", status_code=204)
def remove_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Deletes a clothing item and its associated image file.

    Args:
        item_id (int): The ID of the item to delete.
        current_user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        None

    Raises:
        HTTPException: If the item does not exist or does not belong to the user.
    """
    stmt = select(Item).where(Item.id == item_id, Item.owner_id == current_user.id)
    item = db.scalar(stmt)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    filename = item.image_filename
    db.delete(item)
    db.commit()

    if filename:
        path = UPLOAD_DIR / filename
        if path.exists():
            try:
                os.remove(path)
            except OSError:
                pass
    return None