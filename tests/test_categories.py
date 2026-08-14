# tests/test_services.py
import pytest

from db.models import Expense, Category
from db.services.categories import get_or_create_category, get_category_list


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


def test_get_categories(session, sample_categories):
    ret = get_category_list(session=session)
    assert len(ret) == 2
