# db/services/expenses.py
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models import Expense, Category
from db.services.categories import get_or_create_category


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
