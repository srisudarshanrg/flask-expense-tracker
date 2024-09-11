from expense_tracker import app, db
from expense_tracker.forms import LoginForm, RegisterForm, SearchExpenseForm, AddExpenseForm
from expense_tracker.models import User, Expenses
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from expense_tracker.functions import HashPassword, CheckPasswordHash
import datetime

@app.route("/")
@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expense_tracker():
    user_details = User.query.filter_by(id=current_user.id).first()

    current_month = datetime.datetime.now()
    current_month = current_month.strftime("%B")

    search_expense_form = SearchExpenseForm()
    add_expense_form = AddExpenseForm()

    expenses = Expenses.query.filter_by(expense_user=current_user.id, month=current_month).all()

    if add_expense_form.validate_on_submit():
        name_entered = add_expense_form.expense.data
        desc_entered = add_expense_form.desc.data
        month_entered = add_expense_form.month.data
        cost_entered = int(add_expense_form.cost.data)

        new_expense = Expenses(
            expense=name_entered,
            desc=desc_entered,
            month=month_entered,
            cost=cost_entered,
            expense_user=current_user.id,
        )

        db.session.add(new_expense)
        db.session.commit()

        flash(f"Expense \"{name_entered}\" for month {month_entered} created")

        return redirect(url_for("expense_tracker"))

    return render_template("home.html",
                           user_details=user_details,
                           search=search_expense_form,
                           expenses=expenses,
                           current_month=current_month,
                           add=add_expense_form,
                           )

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_details = User.query.filter_by(id=current_user.id).first()
    return render_template("profile.html", details=user_details)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username_entered = login_form.username.data
        password_entered = login_form.password.data

        attempted_user = User.query.filter_by(username=username_entered).first()
        if attempted_user and CheckPasswordHash(attempted_user.password, bytes(password_entered, "utf-8")):
            login_user(attempted_user)
            flash(message="You have been logged in successfully", category="success")
            return redirect(url_for("expense_tracker"))
        else:
            flash(message="Incorrect credentials", category="danger")

    return render_template("login.html", form=login_form)

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit() and register_form.errors == {}:
        username_entered = register_form.username.data
        password_entered = register_form.password.data
        password_hash = HashPassword(password_entered).encode("utf-8")
        age_entered = register_form.age.data
        dob_entered = register_form.dob.data

        current_date = datetime.datetime.now()
        join_date = current_date.strftime("%d-%m-%Y")

        new_user = User(
            username=username_entered,
            password=password_hash,
            # dob=datetime.datetime.strptime(dob_entered),
            dob=dob_entered,
            age=int(age_entered),
            join_date=join_date,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        print(current_user)

        return redirect(url_for("expense_tracker"))
    else:
        for error in register_form.errors.values():
            flash(message=f"{error}", category="danger")

    return render_template("register.html", form=register_form)

@app.route("/logout")
def logout():
    logout_user
    flash(message="You have been logged out", category="info")
    return redirect(url_for("login"))