# tests/conftest.py
from datetime import datetime, timezone, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from db.models import User, Category, Expense


@pytest.fixture
def session():
    """Fresh in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_user(session):
    user = User(telegram_id=123, username="Test User")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def sample_categories(session):
    food = Category(name="Food")
    transport = Category(name="Transport")
    session.add_all([food, transport])
    session.commit()
    return {"food": food, "transport": transport}


@pytest.fixture
def sample_expenses(session, sample_user, sample_categories):
    """Creates 3 example expenses for sample_user, spread across a few days."""
    now = datetime.now(timezone.utc)

    expenses = [
        Expense(
            amount=23.50,
            user_id=sample_user.id,
            categories=[sample_categories["food"]],
            timestamp=now - timedelta(days=2),
        ),
        Expense(
            amount=12.00,
            user_id=sample_user.id,
            categories=[sample_categories["transport"]],
            timestamp=now - timedelta(days=1),
        ),
        Expense(
            amount=45.00,
            user_id=sample_user.id,
            categories=[sample_categories["food"], sample_categories["transport"]],
            timestamp=now,
        ),
    ]

    session.add_all(expenses)
    session.commit()
    return expenses
