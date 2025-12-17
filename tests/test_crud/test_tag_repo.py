"""Unit tests for Tag repository operations."""

from sqlalchemy.orm import Session

from app.crud.item_repo import create_item
from app.crud.tag_repo import (
    create_tag,
    get_items_by_tags,
    get_or_create_tag,
    get_tag_by_name,
    link_item_to_tag,
)
from app.crud.user_repo import create_user
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate


def test_create_and_get_tag(db_session: Session):
    """Verifies creation and retrieval of tags."""
    tag_name = "Cold"

    new_tag = create_tag(db_session, tag_name)
    assert new_tag.id is not None
    assert new_tag.name == tag_name

    stored_tag = get_tag_by_name(db_session, tag_name)
    assert stored_tag is not None
    assert stored_tag.id == new_tag.id

    missing_tag = get_tag_by_name(db_session, "NonExistent")
    assert missing_tag is None


def test_get_or_create_tag(db_session: Session):
    """Verifies idempotency of get_or_create_tag."""
    tag_name = "Rainy"

    tag1 = get_or_create_tag(db_session, tag_name)
    assert tag1.name == tag_name

    tag2 = get_or_create_tag(db_session, tag_name)
    assert tag2.id == tag1.id


def test_link_item_to_tag(db_session: Session):
    """Verifies linking an item to a tag."""
    user = create_user(
        db_session, UserCreate(email="tag_test@test.com", password="Password1!")
    )
    item = create_item(
        db_session,
        ItemCreate(description="Coat", image_filename="img.jpg"),
        user.id,
    )

    tag = create_tag(db_session, "Freezing")

    confidence_score = 95
    link = link_item_to_tag(db_session, item.id, tag.id, confidence_score)

    assert link.item_id == item.id
    assert link.tag_id == tag.id
    assert link.confidence == confidence_score


def test_get_items_by_tags(db_session: Session):
    """Verifies retrieval of items via their tags."""
    user = create_user(
        db_session, UserCreate(email="tag_test@test.com", password="Password1!")
    )
    item = create_item(
        db_session,
        ItemCreate(description="Raincoat", image_filename="img.jpg"),
        user.id,
    )

    tag = create_tag(db_session, "Rain")
    link = link_item_to_tag(db_session, item.id, tag.id, 99)

    results = get_items_by_tags(db=db_session, user_id=user.id, tag_names=[tag.name])

    assert len(results) > 0
    assert item in results