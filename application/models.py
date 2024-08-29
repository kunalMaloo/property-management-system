from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from application.database import db


class Clients(db.Model):
    __tablename__ = "Clients"
    Client_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)
    Password = Column(String)


class Properties(db.Model):
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
    Broker = db.relationship("Brokers", secondary="Shows")
    photos = db.relationship("Photos", backref="property")


class Sellers(db.Model):
    __tablename__ = "Sellers"
    Seller_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)
    Password = Column(String)


class Brokers(db.Model):
    __tablename__ = "Brokers"
    License_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Phone_no = Column(Integer)
    Brokerage = Column(Integer)
    Locality = Column(String)
    Password = Column(String)
    Photo = Column(String)
    Properties = db.relationship("Properties", secondary="Shows")


class Holds(db.Model):
    __tablename__ = "Holds"
    Client_ID = Column(Integer, ForeignKey("Clients.Client_ID"), primary_key=True)
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Sells(db.Model):
    __tablename__ = "Sells"
    Seller_ID = Column(Integer, ForeignKey("Sellers.Seller_ID"))
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Shows(db.Model):
    __tablename__ = "Shows"
    License_ID = Column(Integer, ForeignKey("Brokers.License_ID"), primary_key=True)
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)


class Photos(db.Model):
    __tablename__ = "Photos"
    P_ID = Column(Integer, ForeignKey("Properties.P_ID"), primary_key=True)
    Photo_URL = Column(String, primary_key=True)


def isValidUser(userID, password, type):
    admin = {
        "2101036": "Anant",
        "2101032": "Aman",
        "2101035": "Amritjot",
        "2101017": "Aditi",
    }
    if type == "Agent":
        checkList = Brokers.query.all()
        for broker in checkList:
            if str(broker.License_ID) == str(userID) and broker.Password == password:
                return (True, broker.Name)

    elif type == "Client":
        checkList = Clients.query.all()
        for client in checkList:
            if str(client.Client_ID) == str(userID) and client.Password == password:
                return (True, client.Name)

    elif type == "Seller":
        checkList = Sellers.query.all()
        for seller in checkList:
            if str(seller.Seller_ID) == str(userID) and seller.Password == password:
                return (True, seller.Name)

    elif type == "Admin":
        if str(userID) in admin.keys() and password == "clutcher":
            return (True, admin[userID])
    return (False, "")


def checkUser(clientID):
    return True
