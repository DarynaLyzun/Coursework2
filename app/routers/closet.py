"""Closet API router."""
import shutil
import uuid
import os
from pathlib import Path
from typing import Annotated, List, Any

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database.session import get_db
from app.routers.auth import get_current_user
from app.database.models import User, Item, ClothingWeather
from app.crud.item_repo import create_item, delete_item
from app.schemas.item import ItemCreate, ItemResponse
from app.core.utils import CANDIDATE_LABELS, INCOMPATIBLE_KEYWORDS
from app.crud.tag_repo import get_or_create_tag, link_item_to_tag

router = APIRouter()
UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def item_to_response(item: Any) -> dict:
    tags = []
    if hasattr(item, "weather_links"):
        tags = [link.tag.name for link in item.weather_links if link.tag]
    
    return {
        "id": item.id,
        "owner_id": item.owner_id,
        "description": item.description,
        "image_filename": item.image_filename,
        "tags": tags
    }

@router.post("/closet/upload", response_model=ItemResponse)
async def upload_item(
    request: Request,
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid image type.")

    file_extension = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
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
            hypothesis_template="This item is worn when the weather is {}."
        )
        
        for label, score in results.items():
            if label in INCOMPATIBLE_KEYWORDS:
                if any(k in description.lower() for k in INCOMPATIBLE_KEYWORDS[label]):
                    continue

            if score > 70:
                tag = get_or_create_tag(db, label)
                link_item_to_tag(db, new_item.id, tag.id, score)

    db.refresh(new_item)
    return item_to_response(new_item)

@router.get("/closet", response_model=List[ItemResponse])
def get_closet(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    stmt = (
        select(Item)
        .where(Item.owner_id == current_user.id)
        .options(joinedload(Item.weather_links).joinedload(ClothingWeather.tag))
    )
    items = db.scalars(stmt).unique().all()
    
    # Convert using helper
    return [item_to_response(item) for item in items]

@router.delete("/closet/{item_id}", status_code=204)
def remove_item(item_id: int, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
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
            try: os.remove(path)
            except OSError: pass
    return None