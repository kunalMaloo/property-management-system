from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from console_extras.db import Base


class Clients(Base):
    __tablename__ = "Clients"
    Client_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)


class Properties(Base):
    __tablename__ = "Properties"
    P_ID = Column(Integer, primary_key=True, autoincrement=True)
    Address = Column(String)
    Locality = Column(String)
    Area = Column(Integer)
    Price = Column(Integer)
    Rent = Column(Boolean)
    Date_Of_Construction = Column(Date)
    No_Of_Bedrooms = Column(Integer)
    Status = Column(String)
    Sell_Date = Column(Date)
    Sell_Price = Column(Integer)


class Sellers(Base):
    __tablename__ = "Sellers"
    Seller_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)


class Brokers(Base):
    __tablename__ = "Brokers"
    License_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)
    Brokerage = Column(Integer)
    Locality = Column(String)


class Holds(Base):
    __tablename__ = "Holds"
    Client_ID = Column(Integer, ForeignKey("Clients.Client_ID"), primary_key=True)
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Sells(Base):
    __tablename__ = "Sells"
    Seller_ID = Column(Integer, ForeignKey("Sellers.Seller_ID"))
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Shows(Base):
    __tablename__ = "Shows"
    License_ID = Column(Integer, ForeignKey("Brokers.License_ID"), primary_key=True)
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Photos(Base):
    __tablename__ = "Photos"
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)
    Photo_URL = Column(String, primary_key=True)
