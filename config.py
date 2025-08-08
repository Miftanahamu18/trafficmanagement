# config.py
# This file contains the configuration variables for the Flask application.

import os

class Config:
    """
    Configuration class for the Flask app.
    Contains the secret key and the database URI.
    """
    
    # Secret key for session management and security.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_and_long_random_string_for_flask_sessions'
    
    # SQLAlchemy Database URI
    # This tells SQLAlchemy how to connect to the MySQL database.
    # Format: 'mysql+pymysql://<user>:<password>@<host>:<port>/<database_name>'
    # I have used the database details you provided at the bottom of your code.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nawmi1856@localhost:3306/traffic_management'
    
    # This setting is recommended to be set to False to disable a feature of
    # Flask-SQLAlchemy that you don't need, which saves system resources.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
