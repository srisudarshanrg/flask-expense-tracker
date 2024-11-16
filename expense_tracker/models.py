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
    name = db.Column(db.String())
    category = db.Column(db.String(), nullable=False)
    time = db.Column(db.DateTime(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user_relation = db.relationship("User", backref="expense", foreign_keys=[user], lazy=True)

class Budget(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user_relation = db.relationship("User", backref="budget", foreign_keys=[user], lazy=True)

class CategoryColors(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    color = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user_relation = db.relationship("User", backref="expense_color", foreign_keys=[user], lazy=True)