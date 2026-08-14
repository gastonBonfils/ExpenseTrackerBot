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


def get_expenses(
    session: Session,
    user_id: int,
    category_name: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[Expense]:
    """
    Get expenses function, depeding on the arguments it returns
    - all expeneses (no category and no range)
    - expenses of a given category (category and no range)
    - expenses in a time range (range)
    - expenses of a category in a time range (range)
    if start_date is None it goes from the begining
    if end_date is None it goes from right now

    this functions works by rewritting the query

    args:
        session: SQLAlchemy Session
        user_id: id of the user consulting its expenses
        category_name: filter by category
        start_date: begining of range, it defaults to very begining
        end_date: end of range, it defaults to now
    returns:
        query: list of expenses
    """
    query = session.query(Expense).filter(Expense.user_id == user_id)

    if category_name is not None:
        category_name = category_name.title()
        query = query.join(Expense.categories).filter(Category.name == category_name)

    if start_date is not None:
        query = query.filter(Expense.timestamp >= start_date)

    if end_date is not None:
        query = query.filter(Expense.timestamp <= end_date)

    return query.all()
