from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    pwd = db.Column(db.String(), nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expense = db.Column(db.String(), nullable=False)
    expense_desc = db.Column(db.String())
    expense_time = db.Column(db.DateTime(), nullable=False)
    expense_amount = db.Column(db.Integer(), nullable=False)
    expense_user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    expense_user_relation = db.relationship("User", backref="expense", foreign_keys=[expense_user], lazy=True)

class Budget(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    budget_name = db.Column(db.String(), nullable=False)
    budget_amount = db.Column(db.Integer(), nullable=False)
    budget_user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    budget_user_relation = db.relationship("User", backref="budget", foreign_keys=[budget_user], lazy=True)