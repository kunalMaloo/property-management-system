import sys
from console_extras.console_config import consoleConfig
from datetime import date
from console_extras.models import (
    Clients,
    Properties,
    Sellers,
    Brokers,
    Holds,
    Sells,
    Shows,
    Photos,
)
from sqlalchemy import text
from console_extras.db import Base, metadata, session, engine


def printVersion():
    print(consoleConfig.consoleName + " " + consoleConfig.version)


def printHelp():
    printVersion()
    print(
        """
        CONSOLE(1)                             Admin Commands                            CONSOLE(1)

NAME
       console - Database Management

SYNOPSIS
       console [SHORT-OPTION]...

DESCRIPTION
       Make changes or view database for Real Estate Website.

       --tables     -t     display all tables
       
       --create     -c     create a new tuple in the database

       --update     -u     update a tuple in the database

       --delete     -d     delete a tuple from the database

       --manual     -m     enter manual sql query

       --query      -q     query from database

       --help display this help and exit

       --version
              output version information and exit

AUTHOR
       Written by ADITI AGARWAL, AMAN YADAV, AMRITJOT KAUR CHAWLA, ANANT SHARMA.

        """
    )


def showTables():
    print("Tables: ")
    for table in metadata.tables.keys():
        print("#\t", end=" ")
        print(table)


def showTableSchema(table):
    for column in table.__table__.columns:
        print((column.name) + " " + str(column.type))


def tableFromTableName(tableName):
    if tableName.lower() == "clients":
        return Clients
    elif tableName.lower() == "properties":
        return Properties
    elif tableName.lower() == "sellers":
        return Sellers
    elif tableName.lower() == "brokers":
        return Brokers
    elif tableName.lower() == "holds":
        return Holds
    elif tableName.lower() == "photos":
        return Photos
    elif tableName.lower() == "sells":
        return Sells
    elif tableName.lower() == "shows":
        return Shows
    else:
        print("No such table")


def clientInput():
    print("Enter Name")
    name = input()
    print("Enter Phone Number")
    ph_no = int(input())
    return Clients(Name=name, Phone_no=ph_no)


def propertyInput():
    print("Enter Address")
    address = input()
    print("Enter Locality")
    locality = input()
    if locality not in Brokers:
        pass


def createMenu():
    showTables()
    print("Choose Table :")
    tableName = input()
    if tableName.lower() == "clients":
        session.add(clientInput())
        session.commit()
    elif tableName.lower() == "properties":
        session.add(propertyInput())
        session.commit()
    elif tableName.lower() == "sellers":
        session.add(sellerInput())
        session.commit()
    elif tableName.lower() == "brokers":
        session.add(brokerInput())
        session.commit()
    elif tableName.lower() == "holds":
        session.add(holdingInput())
        session.commit()
    elif tableName.lower() == "photos":
        session.add(photoInput())
        session.commit()
    elif tableName.lower() == "sells":
        session.add(sellsInput())
        session.commit()
    else:
        print("No such table")


def updateMenu():
    pass


def deleteMenu():
    pass


def query(argIndex):
    query = None
    if argIndex == n_args - 1:
        print("Enter Your Query:")
        query = text(input())
    else:
        query = text(" ".join(args[argIndex + 1 :]))
        # print(query)
    connection = engine.connect()
    result = connection.execute(query)
    for record in result:
        print(record)


n_args = len(sys.argv)
args = sys.argv
for i in range(n_args):
    if args[i] == "all":
        args[i] = "*"
# print(args)


if n_args == 1:
    pass
else:
    for argIndex in range(1, n_args):
        # print(args[argIndex])
        if args[argIndex] == "--version" or args[argIndex] == "-v":
            printVersion()
            exit(0)
        elif args[argIndex] == "--create" or args[argIndex] == "-c":
            createMenu()
            exit(0)
        elif args[argIndex] == "--update" or args[argIndex] == "-u":
            updateMenu()
            exit(0)
        elif args[argIndex] == "--delete" or args[argIndex] == "-d":
            deleteMenu()
            exit(0)
        elif args[argIndex] == "--help" or args[argIndex] == "-h":
            printHelp()
            exit(0)
        elif args[argIndex] == "--manual" or args[argIndex] == "-m":
            query(argIndex)
            exit(0)
        elif args[argIndex] == "--tables" or args[argIndex] == "-t":
            showTables()
            exit(0)
        else:
            print("Error in command input\n\nConsole --help for more")
            exit(0)
