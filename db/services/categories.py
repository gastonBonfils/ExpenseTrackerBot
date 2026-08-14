# db/services/expenses.py
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models import Expense, Category


def get_or_create_category(
    session: Session,
    category_name: str,
) -> Category:
    """Given a category name it returns it returns its id
        if the category didn't exist yet it creates it
    args:
        session: SQLAlchemy session
        category_name: name of the category to get or create

    returns:
        category: Category item

    """
    # TitleLize the string
    category_name = category_name.title()
    category = session.query(Category).filter_by(name=category_name).first()

    if category is None:
        category = Category(name=category_name)
        session.add(category)
        session.commit()

    return category
