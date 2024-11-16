# HashPassword hashes the password and returns it
import datetime
from flask_login import login_user
from .models import Budget, CategoryColors, Expense, User
from . import db, bcrypt

def HashPassword(pwd: str) -> str:
    hashed_pwd = bcrypt.generate_password_hash(pwd).decode(encoding="utf-8")
    return hashed_pwd

# CheckHashPassword checks if the hased password is the same as the entered password
def CheckHashPassword(hash_pwd: bytes, pwd: str) -> bool:
    return bcrypt.check_password_hash(hash_pwd, bytes(pwd, "utf-8"))

# CreateUser creates the new user in the database
def CreateUser(username: str, email: str, pwd: str) -> str:
    try:
        new_user = User(
            username=username,
            email=email,
            pwd=pwd,
            join_date=datetime.datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return "Your new account has been created successfully!", "success"

    except Exception as exception:
        return f"Failed to create user: {exception}", "danger"

# AuthenticUser authenticates the users credentials before logging the user in
def AuthenticateUser(username: str, pwd: str) -> object:
    user = User.query.filter_by(username=username).first()
    if user:
        if CheckHashPassword(user.pwd, pwd):
            return user
        else:
            return False
    else:
        return False
    
# CreateExpense creates a new expense in the database
def CreateExpense(name: str, category: str, color: str, time: datetime.datetime, date: str, amount: int, user: int) -> str:
    try:
        new_expense = Expense(
            name=name,
            category=category,
            time=time,
            date=date,
            amount=amount,
            user=user,
        )

        db.session.add(new_expense)
        db.session.commit()

        exists = CategoryColors.query.filter_by(category=category, user=user).first()
        if exists != None:
            pass
        else:
            new_category_color = CategoryColors(
                category=category,
                color=color,
                user=user,
            )

            db.session.add(new_category_color)
            db.session.commit()

        return f"Expense \"{name}\" created successfully!", "success"
    except Exception as exception:
        return f"Error in creating expense: {exception}", "danger"
    
# SearchExpense searches for a expense based on a recieved query
def SearchExpense(query: str, user: int):
    results = Expense.query.filter(Expense.name.contains(query)).filter_by(user=user).all()
    result_list = []
    for result in results:
        result_dict = {
            "id": result.id,
            "name": result.name,
            "category": result.category,
            "amount": result.amount,
            "time": result.time.strftime("%H:%M"),
            "date": result.date,
            "user": result.user
        }

        result_list.append(result_dict)

    length = len(result_list)
    
    return length, result_list

# GetBudgets gets all the budgets regarding category from the database
def GetBudgets(user: int) -> list:
    try:
        budget_row = Budget.query.filter_by(user=user).all()
        budget_list = []

        for budget in budget_row:
            budget_dict = {
                "id": budget.id,
                "category": budget.category,
                "amount": budget.amount,
                "user": budget.user,
            }

            budget_list.append(budget_dict)

        return budget_list
    
    except Exception as exception:
        return f"Error getting budgets: {exception}"
    
# CreateBudget creates a budget in the database
def CreateBudget(category: str, amount: int, user: int):
    exists = Budget.query.filter_by(category=category, user=user).first()
    if exists != None:
        exists.amount = amount
        db.session.commit()
        return "Budget for category already exists, so only amount has been updated for the existing category"
    else:
        new_budget = Budget(
            category=category,
            amount=amount,
            user=user
        )

        db.session.add(new_budget)
        db.session.commit()

        return f"Budget has been defined for {category}"