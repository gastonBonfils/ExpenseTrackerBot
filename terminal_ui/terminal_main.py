# terminal_ui/terminal_main.py

from db.database import SessionLocal, init_db
from db.services.expenses import add_expense

init_db()
session = SessionLocal()


def print_options():
    a = """
    1. Add basic expense (15000, ["food"], user_id=1)
    2. Add custom expense
    """
    print(a)


def add_basic_expense():
    try:
        expense = add_expense(
            session=session, amount=15000, category_names=["food"], user_id=1
        )
        print(f"Added: {expense}")
    except Exception as e:
        print(f"Error when adding expense: {e}")
    finally:
        session.close()


def main():
    while True:
        print_options()
        user_in = input()

        if user_in == "1":
            add_basic_expense()


main()
