from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from expense_tracker.models import User
import datetime

current_month = datetime.datetime.now()
current_month = current_month.strftime("%B")

# LoginForm is the form handling the login form
class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

# RegisterForm is the form handling the register form
class RegisterForm(FlaskForm):
    def validate_username(self, username_attempted):
        check_exists_user = User.query.filter_by(username=username_attempted.data).all()
        if len(check_exists_user) > 0 :
            raise ValidationError(message="This username already exists.")

    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo(fieldname="password")])
    dob = StringField(label="Date of Birth(dd-mm-yyyy)", validators=[DataRequired()])
    age = IntegerField(label="Age(in numbers)", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class AddExpenseForm(FlaskForm):
    expense = StringField(label="Name of Expense", validators=[DataRequired()])
    desc = StringField(label="Description (optional)", validators=[])
    month = SelectField('Month', choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ], validators=[DataRequired()])
    submit = SubmitField(label="Select")
    cost = IntegerField(label="Expense Amount", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class SearchMonthForm(FlaskForm):
    search_month = SelectField('Month', choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ], default=current_month, validators=[DataRequired()])
    submit = SubmitField(label="Select")

class SearchExpenseForm(FlaskForm):
    search_expense = StringField(label="Search", validators=[DataRequired()])
    submit = SubmitField(label="Search")

class SearchMonthForm(FlaskForm):
    search_month = SelectField('Month', choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ], validators=[DataRequired()])
    submit = SubmitField(label="Select")

# class SearchExpenseForm(FlaskForm):
#     search_expense = StringField(label="Search", validators=[DataRequired()])
#     submit = SubmitField(label="Search")

# class DefineBudgetForm(FlaskForm):
#     def_budget = IntegerField(label="Define Budget", validators=[DataRequired()])
#     submit = SubmitField(label="Search")
