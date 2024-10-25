from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SECRET_KEY"] = "b17540d9a1a7e54eedf84ef9"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Login is required to access this page or feature"
login_manager.login_message_category = "info"

bcrypt = Bcrypt(app)

from . import routes