# terminal_ui/terminal_main.py
from datetime import datetime

from db.models import Expense
from db.database import SessionLocal, init_db
from db.services.expenses import add_expense, get_expenses
from db.services.categories import get_category_list

init_db()
session = SessionLocal()


def print_options():
    a = """
    1. Add basic expense (15000, ["food"], user_id=1)
    2. Add custom expense
    3. Get all expenses
    """
    print(a)


def pretty_print_expense(expense: Expense):
    category_names = [c.name for c in expense.categories]
    short_date = expense.timestamp.strftime("%d/%m/%Y")
    print(
        f"$ {expense.amount} | {category_names} on {short_date} | {expense.user_id} | {expense.comment}"
    )


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


def add_custom_expense():
    try:
        amount = float(input("Amount: "))
    except:
        print("Could not turn amount into float")
        return

    categories = []
    while True:
        print("Write categories, leave empty when finished")
        print(f"Current categories: {categories}")
        category = input("Write category: ")
        if category.strip() == "":
            break

        categories.append(category)

    print(f"Chosen categories:  {categories}")

    comment = input("Write a comment: ")
    try:
        user_id = int(input("User id: "))
    except:
        print("Could not parse user id")
        return

    exp = add_expense(
        session=session,
        amount=amount,
        category_names=categories,
        user_id=user_id,
        comment=comment,
    )
    print(exp)


def get_all_expenses():
    exp_list = get_expenses(session=session, user_id=1)
    for e in exp_list:
        pretty_print_expense(e)


def main():
    while True:
        print_options()
        user_in = input()

        if user_in == "1":
            add_basic_expense()
        elif user_in == "2":
            add_custom_expense()
        elif user_in == "3":
            get_all_expenses()


main()
