import os
from application.mysql_config import mysqlConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        + str(mysqlConfig.user)
        + ":"
        + str(mysqlConfig.password)
        + "@"
        + str(mysqlConfig.host)
        + "/"
        + str(mysqlConfig.database)
        + "?charset=utf8mb4"
    )
