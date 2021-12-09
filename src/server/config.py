import os

class Config(object) :
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    DEBUG      = True
    TESTING    = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RDS_ENGINE   = os.environ.get("RDS_ENGINE")
    RDS_HOSTNAME = os.environ.get("RDS_HOSTNAME")
    RDS_USERNAME = os.environ.get("RDS_USERNAME")
    RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
    RDS_PORT     = os.environ.get("RDS_PORT")
    RDS_DB_NAME  = os.environ.get("RDS_DB_NAME")

    SQLALCHEMY_DATABASE_URI = \
        f"{RDS_ENGINE}://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"

    # Simulation parameters.
    COMMUNICATION_LIMIT  = 10.0
    INITIAL_OBSTACLE_NUM = 20
    BOARD_DIMS           = (100, 100)

