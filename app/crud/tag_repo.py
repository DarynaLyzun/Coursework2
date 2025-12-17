"""Data access operations for Weather Tags."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import ClothingWeather, Item, WeatherTag


def get_tag_by_name(db: Session, name: str) -> WeatherTag | None:
    """Retrieves a weather tag by its unique name.

    Args:
        db (Session): The database session.
        name (str): The name of the tag.

    Returns:
        WeatherTag | None: The tag instance if found, otherwise None.
    """
    statement = select(WeatherTag).where(WeatherTag.name == name)
    return db.scalar(statement)


def create_tag(db: Session, name: str) -> WeatherTag:
    """Creates a new weather tag.

    Args:
        db (Session): The database session.
        name (str): The name of the new tag.

    Returns:
        WeatherTag: The created tag instance.
    """
    tag = WeatherTag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_or_create_tag(db: Session, name: str) -> WeatherTag:
    """Retrieves an existing tag or creates a new one if it does not exist.

    Args:
        db (Session): The database session.
        name (str): The name of the tag.

    Returns:
        WeatherTag: The retrieved or created tag instance.
    """
    tag = get_tag_by_name(db, name)
    if not tag:
        tag = create_tag(db, name)
    return tag


def link_item_to_tag(
    db: Session, item_id: int, tag_id: int, confidence: int
) -> ClothingWeather:
    """Associates an item with a weather tag including a confidence score.

    Args:
        db (Session): The database session.
        item_id (int): The ID of the item.
        tag_id (int): The ID of the tag.
        confidence (int): The confidence score of the association.

    Returns:
        ClothingWeather: The created association object.
    """
    link = ClothingWeather(item_id=item_id, tag_id=tag_id, confidence=confidence)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_items_by_tags(
    db: Session, user_id: int, tag_names: list[str]
) -> Sequence[Item]:
    """Retrieves items owned by a user that match any of the provided tags.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        tag_names (list[str]): A list of tag names to filter by.

    Returns:
        Sequence[Item]: A list of matching items.
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