from expense_tracker.models import User

# ValidateUsername validates whether username entered in register form is valid or not
def ValidateUsername(username: str) -> str:
    if username != "":
        check = User.query.filter_by(username=username).all()
        if len(check) > 0:
            return "This username already exists. Please choose another one"
        else:
            if len(username) > 30 or len(username) < 3:
                return "Username cannot be less than 3 characters or more than 30 characters in length"
            else:
                return True
    else:
        return "Username field cannot be empty"

# ValidateEmail validates whether email entered in register form is valid or not
def ValidateEmail(email: str) -> str:
    if email != "":
        check = User.query.filter_by(email=email).all()
        if len(check) > 0:
            return "This email address already has an account on RaptorNotes. Would you like to login instead?"
        else:
            return True
    else:
        return "Email field cannot be empty"

# ValidatePassword validates if password and confirm password are equal in the register form
def ValidatePassword(pwd: str, pwd_confirm: str) -> str:
    if pwd == pwd_confirm:
        return True
    else:
        return "Password has to be equal to confirmed password"