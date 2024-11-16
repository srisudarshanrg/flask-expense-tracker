# HashPassword hashes the password and returns it
import datetime
from flask_login import login_user
from .models import User
from . import db, bcrypt

def HashPassword(pwd: str) -> str:
    hashed_pwd = bcrypt.generate_password_hash(pwd).decode(encoding="utf-8")
    return hashed_pwd

# CheckHashPassword checks if the hased password is the same as the entered password
def CheckHashPassword(hash_pwd: bytes, pwd: str) -> bool:
    return bcrypt.check_password_hash(hash_pwd, bytes(pwd, "utf-8"))

# CreateUser creates the new user in the database
def CreateUser(username: str, email: str, pwd: str) -> str:
    try:
        new_user = User(
            username=username,
            email=email,
            pwd=pwd,
            join_date=datetime.datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return "Your new account has been created successfully!", "success"

    except Exception as exception:
        return f"Failed to create user: {exception}", "danger"

# AuthenticUser authenticates the users credentials before logging the user in
def AuthenticateUser(username: str, pwd: str) -> object:
    user = User.query.filter_by(username=username).first()
    if user:
        if CheckHashPassword(user.pwd, pwd):
            return user
        else:
            return False
    else:
        return False
    