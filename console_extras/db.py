from sqlalchemy.ext.declarative import declarative_base
from console_extras.mysql_config import mysqlConfig

# import pymysql
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://"
    + mysqlConfig.user
    + ":"
    + mysqlConfig.password
    + "@"
    + mysqlConfig.host
    + "/"
    + mysqlConfig.database
    + "?charset=utf8mb4"
)
metadata = MetaData()
metadata.create_all(engine)
metadata.reflect(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
