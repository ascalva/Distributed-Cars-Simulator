import os

class Config(object) :
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    DEBUG      = True
    TESTING    = True
