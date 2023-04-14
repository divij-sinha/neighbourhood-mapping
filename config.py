from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE='Lax'
    SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI']
