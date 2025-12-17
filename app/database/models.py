"""SQLAlchemy database models definition."""

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class User(Base):
    """Represents a registered user in the system.

    Attributes:
        id (int): Primary key ID.
        email (str): Unique email address.
        hashed_password (str): Bcrypt hashed password.
        items (List[Item]): Collection of items owned by the user.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    items: Mapped[List["Item"]] = relationship(back_populates="owner")


class WeatherTag(Base):
    """Represents a weather condition tag (e.g., 'Rain', 'Cold').

    Attributes:
        id (int): Primary key ID.
        name (str): Unique name of the weather condition.
        item_links (List[ClothingWeather]): Association records linking items to this tag.
    """

    __tablename__ = "weather_tags"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    item_links: Mapped[List["ClothingWeather"]] = relationship(back_populates="tag")


class Item(Base):
    """Represents a clothing item in a user's closet.

    Attributes:
        id (int): Primary key ID.
        description (str): User-provided description of the item.
        image_filename (Optional[str]): Filename of the uploaded image.
        owner_id (int): Foreign key to the User table.
        owner (User): The User who owns this item.
        weather_links (List[ClothingWeather]): Association records linking weather tags to this item.
    """

    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    image_filename: Mapped[Optional[str]] = mapped_column(String(255))

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")

    weather_links: Mapped[List["ClothingWeather"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )


class ClothingWeather(Base):
    """Association table linking Items and WeatherTags with a confidence score.

    Attributes:
        item_id (int): Foreign key to the Item table.
        tag_id (int): Foreign key to the WeatherTag table.
        confidence (int): Confidence score of the classification (0-100).
        item (Item): The associated Item.
        tag (WeatherTag): The associated WeatherTag.
    """

    __tablename__ = "clothing_weather"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("weather_tags.id"), primary_key=True)

    confidence: Mapped[int] = mapped_column(Integer, nullable=False)

    item: Mapped["Item"] = relationship(back_populates="weather_links")
    tag: Mapped["WeatherTag"] = relationship(back_populates="item_links")