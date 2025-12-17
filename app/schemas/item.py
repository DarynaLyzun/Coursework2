"""Pydantic schemas for Item data."""

from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base schema for an item."""
    description: str


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    image_filename: Optional[str] = None


class ItemResponse(ItemBase):
    """Schema for item response data.

    Attributes:
        id (int): Item ID.
        owner_id (int): Owner's User ID.
        image_filename (Optional[str]): Filename of the image.
        tags (List[str]): List of associated weather tags.
    """
    id: int
    owner_id: int
    image_filename: Optional[str] = None
    tags: List[str] = []

    class Config:
        """Pydantic configuration."""
        from_attributes = True