import os

DEBUG = True

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

SESSION_COOKIE_NAME = '_s'
# SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SECRET_KEY = 'secret key'
PASSWORD_SECRET = 'password secret'