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
    dob = db.Column(db.String(), nullable=False)
    join_date = db.Column(db.String(), nullable=False)
    expenses = db.relationship("Expenses", backref="user", lazy=True)

class Expenses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expense = db.Column(db.String(), nullable=False)
    month = db.Column(db.String(), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    expense_user = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Note: {self.note_head} is for user whose id is {self.note_user}"