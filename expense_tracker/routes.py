from expense_tracker import app, db
from expense_tracker.forms import LoginForm, RegisterForm
from expense_tracker.models import User, Expenses
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from expense_tracker.functions import HashPassword, CheckPasswordHash
import datetime

@app.route("/")
@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expense_tracker():
    return render_template("home.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        credential_entered = login_form.credential.data
        password_entered = login_form.password.data

        attempted_user_username = User.query.filter_by(username=credential_entered).first()
        attempted_user_email = User.query.filter_by(email=credential_entered).first()
        if attempted_user_username and CheckPasswordHash(attempted_user_username.password, bytes(password_entered, "utf-8")):
            login_user(attempted_user_username)
            flash(message="You have been logged in successfully", category="info")
            return redirect(url_for("expense_tracker"))
        elif attempted_user_email and CheckPasswordHash(attempted_user_email.password, bytes(password_entered, "utf-8")):
            login_user(attempted_user_email)
            flash(message="You have been logged in successfully", category="info")        
            return redirect(url_for("expense_tracker"))
        else:
            flash(message="Incorrect Credentials", category="danger")

    return render_template("login.html", form=login_form)

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username_entered = register_form.username.data

        check_username = User.query.filter_by(username=username_entered).all()

        if len(check_username) > 0:
            flash(message="This username already exists", category="danger")
        else:
            current_date = datetime.datetime.now()
            current_date_formatted = current_date.strftime("%d-%m-%Y")
            hashed_password = HashPassword(password=register_form.password.data)
            new_user = User(
                username=username_entered,
                password=hashed_password,
                dob=register_form.dob.data,
                join_date=current_date_formatted,
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash(message="You have been registered and logged in successfully", category="info")

            return redirect(url_for("expense_tracker"))

    return render_template("register.html", form=register_form)
