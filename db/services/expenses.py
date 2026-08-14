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


def add_expense(
    session: Session,
    amount: float,
    category_names: list[str],
    user_id: int,
    timestamp: datetime = datetime.now(timezone.utc),
    comment: str = "",
) -> Expense:
    """
    Adds an expense to the database

    args:
        session: SQLalchemy session
        amount: money spent, float
        category_names: list of strings of category names
        user_id: id of the user who made the expense (not telegram_id)
        timestamp: time of the expense, it defaults to current time, optional
        comment: string as a note on the expense, optional

    returns:
        expense

    """

    # delete repeteated categories from the list
    normalized = [c.strip().capitalize() for c in category_names]
    unique = list(dict.fromkeys(normalized))

    # turn category_names into category objects from models.py
    category_instances = [
        get_or_create_category(session=session, category_name=c) for c in unique
    ]

    expense = Expense(
        amount=amount,
        user_id=user_id,
        comment=comment,
        categories=category_instances,
        timestamp=timestamp,
    )

    try:
        session.add(expense)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return expense
