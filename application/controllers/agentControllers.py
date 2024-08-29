from flask import current_app as app, session, request, url_for, redirect, flash
from flask import render_template
from application.models import (
    Properties,
    isValidUser,
    checkUser,
    Holds,
    Brokers,
    Shows,
    Clients,
    Sellers,
    Sells,
)
from application.database import db
from datetime import date


@app.route("/agent/<agentID>/dashboard")
def agent(agentID):
    if (
        "type" in session.keys()
        and session["type"] == "Agent"
        and agentID == session["userID"]
    ):
        agentProperties = (
            Properties.query.join(Shows).filter(Shows.License_ID == agentID).all()
        )
        recentlySoldProperties = (
            Properties.query.join(Shows)
            .filter(Shows.License_ID == agentID)
            .filter(Properties.Status == "Sold")
            .filter(Properties.Sell_Price != None)
            .order_by(Properties.Sell_Date.desc())
            .all()
        )

        sale = sum([property.Sell_Price for property in recentlySoldProperties])

        numberOfProperties = len(agentProperties)

        return render_template(
            "agent/agent.html",
            numberOfProperties=numberOfProperties,
            recently_sold_properties=recentlySoldProperties,
            numberOfCustomers=numberOfProperties,
            sale=sale,
            agentID=agentID,
        )
    else:
        return redirect(url_for("home"))


@app.route("/agent/<agentID>/profile")
def agentProfile(agentID):
    if (
        "type" in session.keys()
        and session["type"] == "Agent"
        and agentID == session["userID"]
    ):
        broker = Brokers.query.filter(Brokers.License_ID == agentID).first()
        return render_template("agent/profile.html", broker=broker)
    else:
        return redirect(url_for("home"))


@app.route("/agent/<agentID>")
def agentProfileSimple(agentID):
    broker = Brokers.query.filter(Brokers.License_ID == agentID).first()
    return render_template("agent/profileSimple.html", broker=broker)


@app.route("/agent/<agentID>/properties", methods=["GET", "POST"])
def agentProperties(agentID):
    if (
        "type" in session.keys()
        and session["type"] == "Agent"
        and agentID == session["userID"]
    ):
        if request.method == "GET":
            soldProperties = (
                Properties.query.join(Shows)
                .filter(Shows.License_ID == agentID)
                .filter(Properties.Status == "Sold")
                .all()
            )
            pendingProperties = (
                Properties.query.join(Shows)
                .filter(Shows.License_ID == agentID)
                .filter(Properties.Status == "Available")
                .all()
            )
            return render_template(
                "agent/properties.html",
                agentID=agentID,
                pendingProperties=pendingProperties,
                soldProperties=soldProperties,
            )
        elif request.method == "POST":
            price = request.form["sellingPrice"]
            id = request.form["clientID"]
            pid = request.form["PID"]
            if checkUser(id):
                db.session.add(Holds(Client_ID=id, P_ID=pid))
                db.session.commit()
                property = Properties.query.filter(Properties.P_ID == pid).first()
                property.Sell_Date = date.today()
                property.Sell_Price = price
                property.Status = "Sold"
                db.session.commit()
            return redirect(url_for("agentProperties", agentID=agentID))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/agent/<agentID>/customers")
def agentCustomers(agentID):
    if (
        "type" in session.keys()
        and session["type"] == "Agent"
        and agentID == session["userID"]
    ):
        clients = (
            Clients.query.join(Holds, Holds.Client_ID == Clients.Client_ID)
            .join(Properties, Properties.P_ID == Holds.P_ID)
            .join(Shows, Shows.P_ID == Properties.P_ID)
            .filter(Shows.License_ID == agentID)
            .all()
        )
        sellers = (
            Sellers.query.join(Sells)
            .join(Properties, Properties.P_ID == Sells.P_ID)
            .join(Shows, Shows.P_ID == Properties.P_ID)
            .filter(Shows.License_ID == agentID)
            .all()
        )
        return render_template(
            "agent/customers.html", agentID=agentID, clients=clients, sellers=sellers
        )
    else:
        return redirect(url_for("home"))
