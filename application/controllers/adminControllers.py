from flask import current_app as app, session, request, url_for, redirect, flash
from flask import render_template
from sqlalchemy import func
from application.database import db
from application.models import (
    Properties,
    Holds,
    Brokers,
)


@app.route("/admin/dashboard")
def admin():
    net_payment = 0
    net_rent = 0
    net_pending = 0
    soldProperties = (
        Properties.query.join(Holds).filter(Properties.Sell_Date != None).all()
    )
    unsoldProperties = (
        Properties.query.join(Holds).filter(Properties.Status == "Available").all()
    )
    print(unsoldProperties)

    properties = (
        Properties.query.filter(Properties.Sell_Date != None)
        .order_by(Properties.Sell_Date.desc())
        .limit(6)
        .all()
    )

    bestPrice = (
        Properties.query.filter(Properties.Status == "sold")
        .filter(Properties.Sell_Date != None)
        .order_by(Properties.Sell_Price.desc())
        .first()
    )

    quantityBroker = (
        db.session.query(Brokers, func.count(Properties.P_ID))
        .filter(Properties.Broker.any())
        .filter(Properties.Status == "sold")
        .group_by(Brokers)
        .order_by(func.count(Properties.P_ID).desc())
        .first()
    )

    qualityBroker = (
        db.session.query(Brokers)
        .join(Brokers.Properties)
        .filter(Properties.Status == "sold")
        .order_by(Properties.Sell_Price.desc())
        .first()
    )
    numberOfLocalities = len(Brokers.query.all())

    # candidates = Brokers.query.filter(Brokers.Properties)

    for property in soldProperties:
        if property.Rent == True:
            net_rent += property.Sell_Price
        net_payment += property.Sell_Price

    for property in unsoldProperties:
        net_pending += property.Price
    return render_template(
        "admin/admin.html",
        net_payment=net_payment,
        net_rent=net_rent,
        net_pending=net_pending,
        properties=properties,
        bestPrice=bestPrice.Sell_Price,
        numberOfLocalities=numberOfLocalities,
        qualityBroker=qualityBroker,
        quantityBroker=quantityBroker,
    )


@app.route("/admin/agents")
def agents():
    brokers = Brokers.query.all()
    return render_template("admin/agents.html", brokers=brokers)


@app.route("/admin/settings")
def adminSettings():
    return render_template("admin/settings.html")
