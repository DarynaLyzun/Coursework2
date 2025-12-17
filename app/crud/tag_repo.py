"""CRUD operations for Weather Tags."""
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import WeatherTag, ClothingWeather, Item

def get_tag_by_name(db: Session, name: str) -> WeatherTag | None:
    """Retrieves a tag by its name.

    Args:
        db (Session): The database session.
        name (str): The name of the weather tag (e.g., "Cold").

    Returns:
        WeatherTag | None: The tag object if found, otherwise None.
    """
    statement = select(WeatherTag).where(WeatherTag.name == name)
    return db.scalar(statement)

def create_tag(db: Session, name: str) -> WeatherTag:
    """Creates a new weather tag in the database.

    Args:
        db (Session): The database session.
        name (str): The name of the new tag.

    Returns:
        WeatherTag: The created tag object.
    """
    tag = WeatherTag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_or_create_tag(db: Session, name: str) -> WeatherTag:
    """Retrieves a tag if it exists, otherwise creates it.

    This helper function ensures that we don't create duplicate tags
    for the same weather condition.

    Args:
        db (Session): The database session.
        name (str): The name of the tag.

    Returns:
        WeatherTag: The existing or newly created tag.
    """
    tag = get_tag_by_name(db, name)
    if not tag:
        tag = create_tag(db, name)
    return tag

def link_item_to_tag(db: Session, item_id: int, tag_id: int, confidence: int) -> ClothingWeather:
    """Links an item to a weather tag with a confidence score.

    Args:
        db (Session): The database session.
        item_id (int): The ID of the clothing item.
        tag_id (int): The ID of the weather tag.
        confidence (int): The AI's confidence score (0-100).

    Returns:
        ClothingWeather: The created association record.
    """
    link = ClothingWeather(
        item_id=item_id, 
        tag_id=tag_id, 
        confidence=confidence
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def get_items_by_tags(db: Session, user_id: int, tag_names: list[str]) -> Sequence[Item]:
    """Retrieves clothing items that match the given weather tags for a specific user.

    Performs a join across Item, ClothingWeather, and WeatherTag to find items
    owned by the user that are associated with any of the provided tag names.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user who owns the items.
        tag_names (list[str]): A list of weather tag names (e.g., ["Cold", "Rain"]).

    Returns:
        Sequence[Item]: A list of matching clothing items.
    """
    statement = (
        select(Item)
        .join(ClothingWeather, Item.id == ClothingWeather.item_id)
        .join(WeatherTag, ClothingWeather.tag_id == WeatherTag.id)
        .where(Item.owner_id == user_id)
        .where(WeatherTag.name.in_(tag_names))
        .distinct()
    )
    return db.scalars(statement).all()