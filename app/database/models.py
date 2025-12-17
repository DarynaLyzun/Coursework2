"""Database models for the Weather Closet application."""

from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    items: Mapped[List["Item"]] = relationship(back_populates="owner")

class WeatherTag(Base):
    __tablename__ = "weather_tags"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    item_links: Mapped[List["ClothingWeather"]] = relationship(back_populates="tag")

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    image_filename: Mapped[Optional[str]] = mapped_column(String(255))
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")

    weather_links: Mapped[List["ClothingWeather"]] = relationship(
        back_populates="item", 
        cascade="all, delete-orphan"
    )

class ClothingWeather(Base):
    __tablename__ = "clothing_weather"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("weather_tags.id"), primary_key=True)
    
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)

    item: Mapped["Item"] = relationship(back_populates="weather_links")
    tag: Mapped["WeatherTag"] = relationship(back_populates="item_links")