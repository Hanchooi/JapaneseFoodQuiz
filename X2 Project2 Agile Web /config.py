import os
basedir = os.path.abspath(os.path.dirname(__file__))
import sqlite3

class Config(object):

    # Creation of secret key for WTForms
    SECRET_KEY = os.environ.get('SERCRET_KEY') or "123-key"

    # Set specs for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db'+"?check_same_thread=False")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


