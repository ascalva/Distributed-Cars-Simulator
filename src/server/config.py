import os

class Config(object) :
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    DEBUG      = True
    TESTING    = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    # Simulation parameters.
    COMMUNICATION_LIMIT = 2

    BOARD_WIDTH  = 10
    BOARD_HEIGHT = 10
