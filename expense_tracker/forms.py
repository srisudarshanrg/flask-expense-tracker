from flask_wtf import FlaskForm
from wtforms import IntegerField, validators, StringField, PasswordField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from expense_tracker.models import User

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

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

