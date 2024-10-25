from flask import redirect, render_template, request, flash, url_for
from .functions import AuthenticateUser, CreateUser, HashPassword
from validations.register_validations import ValidateEmail, ValidatePassword, ValidateUsername
from . import app, db, login_manager
from flask_login import login_required, login_user, logout_user

# home is the handler for the home page
@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

# profile is the handler for the profile page
@app.route("/profile")
@app.route("/user")
@login_required
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
            
            if user != None:
                login_user(user)
                flash(message="You have been logged in successfully!", category="success")
                return redirect(url_for('home'))
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

            if results[0] == "True" and results[1] == "True" and results[2] == "True":
                hash_pwd = HashPassword(pwd)
                msg, category = CreateUser(username, email, hash_pwd)

                flash(message=msg, category=category)
                return redirect(url_for('home'))
            else:
                for result in results:
                    if result != "True":
                        flash(f"{result}", category="danger")
                    else:
                        print("checking")

    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))
    