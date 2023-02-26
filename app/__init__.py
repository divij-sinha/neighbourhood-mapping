from flask import Flask
from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
# from flask_login import LoginManager
# from sqlcipher3 import dbapi2 as sqlite3

app = Flask(__name__)
app.config.from_object(Config)
#db = SQLAlchemy(app, engine_options={'module':sqlite3})
#migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'

from app import routes