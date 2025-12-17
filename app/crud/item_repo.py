"""CRUD operations for Item management.

This module provides the database interactions for creating, retrieving,
and managing clothing items within the user's closet.
"""

from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.schemas.item import ItemCreate
from app.database.models import Item, ClothingWeather

def create_item(db: Session, item: ItemCreate, owner_id: int) -> Item:
    """Creates a new clothing item in the database.

    Args:
        db (Session): The database session.
        item (ItemCreate): The item data (description, image filename).
        owner_id (int): The ID of the user who owns this item.

    Returns:
        Item: The created SQLAlchemy Item object.
    """
    new_item = Item(
        description=item.description, 
        image_filename=item.image_filename, 
        owner_id=owner_id
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item

def get_items_by_user(db: Session, user_id: int) -> Sequence[Item]:
    """Retrieves all items owned by a specific user."""
    statement = (
        select(Item)
        .where(Item.owner_id == user_id)
        .options(joinedload(Item.weather_links).joinedload(ClothingWeather.tag))
    )
    return db.scalars(statement).unique().all()

def delete_item(db: Session, item_id: int, owner_id: int) -> bool:
    """Deletes an item if it belongs to the user."""
    item = db.scalar(select(Item).where(Item.id == item_id, Item.owner_id == owner_id))
    
    if not item:
        return False
        
    db.delete(item)
    db.commit()
    return True