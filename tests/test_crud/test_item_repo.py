"""Unit tests for Item repository operations."""

from sqlalchemy.orm import Session

from app.crud.item_repo import create_item, delete_item, get_items_by_user
from app.crud.user_repo import create_user
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate


def test_create_item(db_session: Session):
    """Verifies correct item creation and ownership.

    Args:
        db_session (Session): The database session fixture.
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


def test_get_items_by_user(db_session: Session):
    """Verifies retrieval of items belonging to a specific user.

    Args:
        db_session (Session): The database session fixture.
    """
    user1 = create_user(
        db_session, UserCreate(email="user1@example.com", password="Password1!")
    )
    user2 = create_user(
        db_session, UserCreate(email="user2@example.com", password="Password1!")
    )

    create_item(
        db_session,
        ItemCreate(description="Item 1", image_filename="1.jpg"),
        user1.id,
    )
    create_item(
        db_session,
        ItemCreate(description="Item 2", image_filename="2.jpg"),
        user1.id,
    )

    create_item(
        db_session,
        ItemCreate(description="Item 3", image_filename="3.jpg"),
        user2.id,
    )

    items_user1 = get_items_by_user(db_session, user1.id)
    items_user2 = get_items_by_user(db_session, user2.id)

    assert len(items_user1) == 2
    assert len(items_user2) == 1
    assert items_user1[0].owner_id == user1.id


def test_delete_item_success(db_session: Session):
    """Verifies that an item can be successfully deleted by its owner.

    Args:
        db_session (Session): The database session fixture.
    """
    user = create_user(
        db_session, UserCreate(email="del@example.com", password="Password1!")
    )
    item = create_item(
        db_session,
        ItemCreate(description="To Delete", image_filename="del.jpg"),
        user.id,
    )

    result = delete_item(db_session, item.id, user.id)
    assert result is True

    items = get_items_by_user(db_session, user.id)
    assert len(items) == 0


def test_delete_item_failure_wrong_owner(db_session: Session):
    """Verifies that a user cannot delete another user's item.

    Args:
        db_session (Session): The database session fixture.
    """
    owner = create_user(
        db_session, UserCreate(email="owner@example.com", password="Password1!")
    )
    hacker = create_user(
        db_session, UserCreate(email="hacker@example.com", password="Password1!")
    )

    item = create_item(
        db_session,
        ItemCreate(description="Safe", image_filename="safe.jpg"),
        owner.id,
    )

    result = delete_item(db_session, item.id, hacker.id)
    assert result is False

    items = get_items_by_user(db_session, owner.id)
    assert len(items) == 1