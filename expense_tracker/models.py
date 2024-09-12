from expense_tracker import db
from expense_tracker import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True)
    password = db.Column(db.String(), nullable=False)
    dob = db.Column(db.DateTime(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)
    expenses = db.relationship("Expenses", backref="user", lazy=True)

class Expenses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expense = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String(), nullable=False)
    month = db.Column(db.String(), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    expense_user = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Note: {self.note_head} is for user whose id is {self.note_user}"
    
class Budget(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    budget = db.Column(db.Integer(), nullable=False)
    budget_month = db.Column(db.String(), nullable=False)
    budget_year = db.Column(db.Integer(), nullable=False)
    budget_user = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"This budget is for user of user id {self.budget_user} for the month {self.budget_month}"