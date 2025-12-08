"""Unit tests for Item CRUD operations.

This module verifies that the database repository functions correctly handle
creating and managing clothing items, ensuring they are properly associated
with their owners.
"""

from sqlalchemy.orm import Session
from app.crud.item_repo import create_item
from app.crud.user_repo import create_user
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate

def test_create_item(db_session: Session):
    """Verifies that an item can be created and linked to a user.

    Ensures that:
    1. A user is created to act as the owner.
    2. The item is persisted to the database.
    3. The item's owner_id strictly matches the creating user's ID.
    """
    email = "newuser@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    user = create_user(db_session, user_in)
    
    description = "Some description string"
    image_filename = "some_filename.jpg"
    item_in = ItemCreate(description=description, image_filename=image_filename)

    item = create_item(db_session, item_in, user.id)

    assert item.owner_id == user.id
    assert item.description == description
    assert item.image_filename == image_filename