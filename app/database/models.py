"""Database models for the Weather Closet application.

This module defines the SQLAlchemy ORM models used to represent users,
clothing items, and weather tags. It utilizes SQLAlchemy 2.0 style
mappings and type hints.
"""

from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

class User(Base):
    """Represents a registered user of the application.

    Attributes:
        id (int): The unique primary key identifier.
        email (str): The user's email address. Must be unique.
        hashed_password (str): The securely hashed password string.
        items (List[Item]): A list of clothing items owned by this user.
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    items: Mapped[List["Item"]] = relationship(back_populates="owner")

class WeatherTag(Base):
    """Represents a specific weather condition derived from AI analysis.

    Attributes:
        id (int): The unique primary key identifier.
        name (str): The name of the tag (e.g., 'Rain', 'Cold'). Must be unique.
        item_links (List[ClothingWeather]): The association objects linking this
            tag to specific items.
    """
    __tablename__ = "weather_tags"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    item_links: Mapped[List["ClothingWeather"]] = relationship(back_populates="tag")

class Item(Base):
    """Represents a single piece of clothing in a user's closet.

    Attributes:
        id (int): The unique primary key identifier.
        description (str): Text description of the item used for AI analysis.
        image_filename (str): The file path to the stored image.
        owner_id (int): Foreign key linking to the User who owns this item.
        owner (User): The User object corresponding to the owner_id.
        weather_links (List[ClothingWeather]): A list of association objects
            linking this item to weather tags.
    """
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    image_filename: Mapped[Optional[str]] = mapped_column(String(255))
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")

    weather_links: Mapped[List["ClothingWeather"]] = relationship(back_populates="item")

class ClothingWeather(Base):
    """Association Object linking an Item to a WeatherTag with a confidence score.

    This class serves as the 'through' table for the many-to-many relationship
    between Items and WeatherTags, allowing us to store the AI's confidence
    level for each prediction.

    Attributes:
        item_id (int): Foreign key to the items table. Part of composite PK.
        tag_id (int): Foreign key to the weather_tags table. Part of composite PK.
        confidence (float): A value between 0.0 and 1.0 indicating how confident
            the AI is that this tag applies to the item.
        item (Item): The related Item object.
        tag (WeatherTag): The related WeatherTag object.
    """
    __tablename__ = "clothing_weather"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("weather_tags.id"), primary_key=True)
    
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)

    item: Mapped["Item"] = relationship(back_populates="weather_links")
    tag: Mapped["WeatherTag"] = relationship(back_populates="item_links")