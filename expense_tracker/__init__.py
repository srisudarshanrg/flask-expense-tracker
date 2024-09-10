from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///expense_tracker.db"
app.config['SECRET_KEY'] = "3bd7e299f5c85baff143fb40"

db = SQLAlchemy(app)
app.app_context().push()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from expense_tracker import routes
