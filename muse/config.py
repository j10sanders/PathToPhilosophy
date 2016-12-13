import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:musespace@localhost:5432/musing"
    DEBUG = True