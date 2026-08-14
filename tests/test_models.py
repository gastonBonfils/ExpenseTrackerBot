# tests/test_models.py
import pytest

from db.models import Expense, Category


@pytest.fixture
def sample_expense(session):
    expense = Expense(amount=23.50, category_names=["food"])
    session.add(expense)
    session.commit()
    return expense


def test_expense_requires_amount(session):
    expense = Expense()  # no amount provided
    session.add(expense)
    with pytest.raises(Exception):  # IntegrityError, since nullable=False
        session.commit()


def test_expense_can_have_multiple_categories():
    food = Category(name="food")
    household = Category(name="household")

    expense = Expense(amount=45.00)
    expense.categories.append(food)
    expense.categories.append(household)

    assert len(expense.categories) == 2
    assert food in expense.categories
    assert household in expense.categories
