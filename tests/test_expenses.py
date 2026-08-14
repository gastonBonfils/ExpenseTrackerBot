# tests/test_services.py
from datetime import datetime, timezone, timedelta

import pytest

from db.models import Expense, Category
from db.services.expenses import add_expense, get_expenses

# @pytest.fixture
# def simple_expense():


## Expenses
def test_adding_expense_success(session):
    ret = add_expense(session, amount=1500, category_names=["Transport"], user_id=1)

    saved = session.query(Expense).first()
    assert saved is not None
    assert saved.amount == 1500
    # the category should be created since it's a new one
    assert saved.categories[0].name == "Transport"


# def test_adding_expense_failure(session):
#     # missing user_id
#     with pytest.raises(TypeError):
#         add_expense(session, amount=1500, category_names=["food"])

#     session.expire_all()
#     assert session.query(Expense).count() == 0

#     # missing category
#     with pytest.raises(TypeError):
#         add_expense(session, amount=1500, user_id=1)

#     session.expire_all()
#     assert session.query(Expense).count() == 0


def test_adding_expense_multiple_category(session):
    ret = add_expense(
        session=session, amount=25000, category_names=["food", "party"], user_id=1
    )
    saved = session.query(Expense).first()
    assert len(saved.categories) == 2
    category_names = [c.name for c in saved.categories]
    assert "Food" in category_names
    assert "Party" in category_names


def test_adding_expense_repeated_category(session):
    ret = add_expense(
        session=session, amount=1500, category_names=["food", "FOOD"], user_id=1
    )
    saved = session.query(Expense).first()
    assert len(saved.categories) == 1


# test for comments
def test_expense_comment(session):
    rat = add_expense(
        session=session,
        amount=23000,
        category_names=["food"],
        user_id=1,
        comment="hamburguer",
    )

    saved = session.query(Expense).first()
    assert saved.comment == "hamburguer"


# def test_check_state(session):
#     ret = add_expense(session, amount=1500, category_names=["food"], user_id=1)

#     items = session.query(Expense).count()
#     assert items == 1

# test for getting expenses


def test_get_expenses(session, sample_user, sample_expenses):
    expenses = get_expenses(session=session, user_id=sample_user.id)
    assert len(expenses) == 3


def test_get_categories(session, sample_user, sample_expenses, sample_categories):
    exp1 = get_expenses(session=session, user_id=sample_user.id, category_name="FOOD")
    assert len(exp1) == 2
    exp2 = get_expenses(
        session=session, user_id=sample_user.id, category_name="TRANSPORT"
    )
    assert len(exp2) == 2

    exp3 = get_expenses(
        session=session, user_id=sample_user.id, category_name="Non Existant"
    )
    assert len(exp3) == 0


def test_get_time_ranges(session, sample_user, sample_expenses, sample_categories):
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    yesterday_sod = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    before_yesterday = yesterday - timedelta(days=1)
    before_yesterday_sod = before_yesterday.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    exp1 = get_expenses(
        session=session,
        user_id=sample_user.id,
        start_date=yesterday_sod,
        end_date=now,
    )
    assert len(exp1) == 2

    exp2 = get_expenses(
        session=session,
        user_id=sample_user.id,
        start_date=before_yesterday_sod,
        end_date=now,
        category_name="food",
    )
    assert len(exp2) == 2

    # invalid range
    exp3 = get_expenses(
        session=session,
        user_id=sample_user.id,
        start_date=now,
        end_date=before_yesterday_sod,
    )
    assert len(exp3) == 0

    exp4 = get_expenses(
        session=session,
        user_id=sample_user.id,
        start_date=now,
        end_date=now,
    )
    assert len(exp4) == 0

    exp5 = get_expenses(session=session, user_id=2)
    assert len(exp5) == 0
