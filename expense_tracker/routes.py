from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from . import app
from .functions import AuthenticateUser, CreateUser, HashPassword
from .validations import ValidateEmail, ValidatePassword, ValidateUsername

# expenses is the handler for the expenses page
@app.route("/")
@app.route("/expenses")
@login_required
def expenses():
    return render_template("expenses.html")

@app.route("/tracker")
@login_required
def tracker():
    return render_template("tracker.html")

@app.route("/budget")
@login_required
def budget():
    return render_template("budget.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# login is the handler for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "loginForm" in request.form:
            username = request.form.get("username")
            pwd = request.form.get("pwd")

            user = AuthenticateUser(username, pwd)
            
            if user != False:
                login_user(user)
                flash(message="You have been logged in successfully!", category="success")
                return redirect(url_for('expenses'))
            else:
                flash(message="Invalid credentials", category="danger")

    return render_template("login.html")

# register is the handler for the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "registerForm" in request.form:
            username = request.form.get("username")
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            pwd_confirm = request.form.get("pwd-confirm")

            username_validation =  ValidateUsername(username)
            email_validation = ValidateEmail(email)
            pwd_validation = ValidatePassword(pwd, pwd_confirm)

            results = [username_validation, email_validation, pwd_validation]

            if results[0] == True and results[1] == True and results[2] == True:
                hash_pwd = HashPassword(pwd)
                msg, category = CreateUser(username, email, hash_pwd)

                flash(message=msg, category=category)
                return redirect(url_for('expenses'))
            else:
                for result in results:
                    if result != True:
                        flash(f"{result}", category="danger")
                    else:
                        print(result)

    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))
    