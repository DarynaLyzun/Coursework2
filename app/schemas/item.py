"""Pydantic schemas for Item data validation."""

from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base schema for item data.

    Attributes:
        description (str): Text description of the item.
    """

    description: str


class ItemCreate(ItemBase):
    """Schema for creating a new item.

    Attributes:
        image_filename (Optional[str]): The filename of the item's image.
    """

    image_filename: Optional[str] = None


class ItemResponse(ItemBase):
    """Schema for item response data.

    Attributes:
        id (int): The unique ID of the item.
        owner_id (int): The ID of the item's owner.
        image_filename (Optional[str]): The filename of the item's image.
        tags (List[str]): A list of associated weather tags.
    """

    id: int
    owner_id: int
    image_filename: Optional[str] = None
    tags: List[str] = []

    class Config:
        """Pydantic configuration."""
        from_attributes = True