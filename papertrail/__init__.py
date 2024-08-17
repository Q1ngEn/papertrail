from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e52751703579269d27d78a5b0957e6a6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///papertrail.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'  # style of message

with app.app_context():
    db.create_all()

from papertrail import routes
