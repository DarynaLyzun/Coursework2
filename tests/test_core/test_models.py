"""Unit tests for database models."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models import ClothingWeather, Item, User, WeatherTag


def test_create_user_item_relationship(db_session: Session):
    """Verifies that a user can own items."""
    new_user = User(email="student@example.com", hashed_password="securepassword")
    db_session.add(new_user)
    db_session.commit()

    parka = Item(description="Blue Winter Parka", owner=new_user)
    db_session.add(parka)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(email="student@example.com").first()

    assert saved_user is not None
    assert len(saved_user.items) == 1
    assert saved_user.items[0].description == "Blue Winter Parka"


def test_clothing_weather_confidence_score(db_session: Session):
    """Verifies confidence score persistence in item-tag relationships."""
    user = User(email="tester@example.com", hashed_password="pw")
    item = Item(description="Raincoat", owner=user)
    tag = WeatherTag(name="Rain")

    db_session.add_all([user, item, tag])
    db_session.commit()

    link = ClothingWeather(item=item, tag=tag, confidence=0.98)
    db_session.add(link)
    db_session.commit()

    assert len(item.weather_links) == 1
    assert item.weather_links[0].tag.name == "Rain"
    assert item.weather_links[0].confidence == 0.98


def test_user_email_must_be_unique(db_session: Session):
    """Verifies uniqueness constraint on user email."""
    user1 = User(email="duplicate@example.com", hashed_password="pw1")
    db_session.add(user1)
    db_session.commit()

    user2 = User(email="duplicate@example.com", hashed_password="pw2")
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_weather_tag_name_must_be_unique(db_session: Session):
    """Verifies uniqueness constraint on weather tag name."""
    tag1 = WeatherTag(name="Rain")
    db_session.add(tag1)
    db_session.commit()

    tag2 = WeatherTag(name="Rain")
    db_session.add(tag2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_prevent_duplicate_tags_on_item(db_session: Session):
    """Verifies that duplicate tags cannot be assigned to the same item."""
    user = User(email="unique@test.com", hashed_password="pw")
    item = Item(description="Scarf", owner=user)
    tag = WeatherTag(name="Windy")

    db_session.add_all([user, item, tag])
    db_session.commit()

    link1 = ClothingWeather(item=item, tag=tag, confidence=0.80)
    db_session.add(link1)
    db_session.commit()

    link2 = ClothingWeather(item=item, tag=tag, confidence=0.99)
    db_session.add(link2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_cannot_delete_user_with_items(db_session: Session):
    """Verifies that users with existing items cannot be deleted without cascade."""
    user = User(email="victim@test.com", hashed_password="pw")
    item = Item(description="Beloved Shirt", owner=user)
    db_session.add_all([user, item])
    db_session.commit()

    db_session.delete(user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()