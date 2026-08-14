# tests/test_services.py
import pytest

from db.models import Expense, Category
from db.services.expenses import add_expense, get_or_create_category

# @pytest.fixture
# def simple_expense():


# category creation
def test_creating_new_category(session):
    ret = get_or_create_category(session=session, category_name="food")

    assert ret is not None
    assert ret.name == "Food"
    assert ret.id == 1

    saved = session.query(Category).first()
    assert saved is not None
    assert saved.name == "Food"


def test_creating_repeated_category(session):
    ret1 = get_or_create_category(session=session, category_name="food")
    ret2 = get_or_create_category(session=session, category_name="FOOD")

    assert session.query(Category).count() == 1
    assert ret1.name == "Food"
    assert ret1.id == 1

    assert ret2.name == "Food"
    assert ret2.id == 1


def test_creating_multiple_categories(session):
    ret1 = get_or_create_category(session=session, category_name="food")
    ret2 = get_or_create_category(session=session, category_name="Transport")

    assert session.query(Category).count() == 2
    assert ret1.name == "Food"
    assert ret1.id == 1

    assert ret2.name == "Transport"
    assert ret2.id == 2


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
