"""Unit tests for Tag CRUD operations.

This module verifies that the database repository functions correctly handle
creating, retrieving, and linking weather tags to clothing items.
"""

from sqlalchemy.orm import Session
from app.crud.tag_repo import create_tag, get_tag_by_name, get_or_create_tag, link_item_to_tag, get_items_by_tags
from app.crud.item_repo import create_item
from app.crud.user_repo import create_user
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate

def test_create_and_get_tag(db_session: Session):
    """Verifies that a tag can be created and retrieved by name.
    
    Ensures that:
    1. A new tag is persisted to the database.
    2. Retrieval by exact name matches the created tag.
    3. Retrieval for a non-existent tag returns None.
    """
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
    """Verifies that get_or_create_tag handles both new and existing tags.
    
    Ensures that:
    1. It creates a tag if it doesn't exist.
    2. It returns the *existing* tag if called again (no duplicates).
    """
    tag_name = "Rainy"
    
    tag1 = get_or_create_tag(db_session, tag_name)
    assert tag1.name == tag_name
    
    tag2 = get_or_create_tag(db_session, tag_name)
    assert tag2.id == tag1.id

def test_link_item_to_tag(db_session: Session):
    """Verifies that an item can be linked to a weather tag with confidence.
    
    This requires setting up the full chain: User -> Item -> Link -> Tag.
    """
    user = create_user(db_session, UserCreate(email="tag_test@test.com", password="Password1!"))
    item = create_item(
        db_session, 
        ItemCreate(description="Coat", image_filename="img.jpg"), 
        user.id
    )
    
    tag = create_tag(db_session, "Freezing")
    
    confidence_score = 95
    link = link_item_to_tag(db_session, item.id, tag.id, confidence_score)
    
    assert link.item_id == item.id
    assert link.tag_id == tag.id
    assert link.confidence == confidence_score
    
def test_get_items_by_tags(db_session: Session):
    """Verifies that items can be retrieved by their associated weather tags.

    Ensures that:
    1. A user, item, and weather tag are correctly created and linked in the database.
    2. The repository function returns the specific item when queried with the matching tag.
    3. The result list contains the expected item data.
    """
    user = create_user(db_session, UserCreate(email="tag_test@test.com", password="Password1!"))
    item = create_item(
        db_session, 
        ItemCreate(description="Raincoat", image_filename="img.jpg"), 
        user.id
    )
    
    tag = create_tag(db_session, "Rain")
    link = link_item_to_tag(db_session, item.id, tag.id, 99)
    
    results = get_items_by_tags(db=db_session, user_id=user.id, tag_names=[tag.name])
    
    assert len(results) > 0
    assert item in results