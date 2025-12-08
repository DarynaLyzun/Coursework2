"""CRUD operations for Item management.

This module provides the database interactions for creating, retrieving,
and managing clothing items within the user's closet.
"""

from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate
from app.database.models import Item

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