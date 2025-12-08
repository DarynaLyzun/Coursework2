"""Pydantic models for Item management.

This module defines the schemas used for creating and retrieving clothing items,
ensuring proper data validation and serialization for the API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    """Shared properties for Item schemas.
    
    Attributes:
        description (str): A text description of the clothing item.
        image_filename (Optional[str]): The path to the image, if one exists.
    """
    description: str
    image_filename: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema for item creation requests.
    
    Inherits all fields from ItemBase. No additional fields are required
    for creation as the owner_id is derived from the current user.
    """
    pass

class ItemResponse(ItemBase):
    """Schema for item API responses.
    
    Attributes:
        id (int): The unique database identifier.
        owner_id (int): The ID of the user who owns this item.
    """
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)