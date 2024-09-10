from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField, EmailField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    credential = StringField(label="Username or Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo(fieldname="password")])
    dob = DateTimeField(label="Date of Birth", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

