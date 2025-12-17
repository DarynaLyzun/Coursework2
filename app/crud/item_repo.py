"""Data access operations for Items."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.models import ClothingWeather, Item
from app.schemas.item import ItemCreate


def create_item(db: Session, item: ItemCreate, owner_id: int) -> Item:
    """Persists a new item in the database.

    Args:
        db (Session): The database session.
        item (ItemCreate): The item creation schema containing description and image.
        owner_id (int): The unique ID of the user who owns the item.

    Returns:
        Item: The created item instance.
    """
    new_item = Item(
        description=item.description,
        image_filename=item.image_filename,
        owner_id=owner_id,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def get_items_by_user(db: Session, user_id: int) -> Sequence[Item]:
    """Retrieves all items belonging to a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The unique ID of the user.

    Returns:
        Sequence[Item]: A list of Item objects owned by the user.
    """
    statement = (
        select(Item)
        .where(Item.owner_id == user_id)
        .options(joinedload(Item.weather_links).joinedload(ClothingWeather.tag))
    )
    return db.scalars(statement).unique().all()


def delete_item(db: Session, item_id: int, owner_id: int) -> bool:
    """Removes an item from the database if it belongs to the specified owner.

    Args:
        db (Session): The database session.
        item_id (int): The unique ID of the item to delete.
        owner_id (int): The unique ID of the user requesting deletion.

    Returns:
        bool: True if the item was found and deleted, False otherwise.
    """
    item = db.scalar(
        select(Item).where(Item.id == item_id, Item.owner_id == owner_id)
    )

    if not item:
        return False

    db.delete(item)
    db.commit()
    return True