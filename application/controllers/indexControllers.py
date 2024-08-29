from flask import (
    current_app as app,
    session,
    request,
    url_for,
    redirect,
    flash,
)
from flask import render_template
from application.models import Properties, isValidUser, Photos, Sells, Brokers
from application.database import db


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        properties = (
            Properties.query.filter(Properties.Status == "Available").join(Photos).all()
        )
        localities = Brokers.query.with_entities(Brokers.Locality.distinct()).all()
        areas = Properties.query.with_entities(Properties.Area.distinct()).all()
        min_area = min(areas)[0]
        max_area = max(areas)[0]
        diff = (max_area - min_area) // 5
        areas = list(range(min_area, max_area + 1, diff))

        if "badlogin" in session.keys():
            session.pop("badlogin")
            flash("Either userID or Password is wrong!")

        print(dict(session).keys(), dict(session).values())
        return render_template(
            "home/index.html", properties=properties, localities=localities, areas=areas
        )
    else:
        return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        user_id = request.form["userID"]
        password = request.form["password"]
        type = request.form["type"]
        validity = isValidUser(user_id, password, type)
        if validity[0]:
            session["userID"] = user_id
            session["type"] = type
            session["username"] = validity[1]
        else:
            session["badlogin"] = True
        if session["type"] == "Admin":
            return redirect(url_for("admin"))
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    if "username" in session.keys():
        session.pop("username")
        session.pop("type")
        session.pop("userID")
    return redirect(url_for("home"))


@app.route("/aboutUs")
def aboutUs():
    return render_template("home/aboutUs.html")


@app.route("/contactUs")
def contactUs():
    return render_template("home/contact.html")


@app.route("/addProperty", methods=["POST", "GET"])
def addProperty():
    if "type" in session.keys() and session["type"] == "Seller":
        if request.method == "GET":
            return render_template("home/addProp.html")
        elif request.method == "POST":
            address = request.form["address"]
            locality = request.form["locality"]
            area = request.form["area"]
            price = request.form["price"]
            yearOfConstruction = request.form["yearOfConstruction"]
            rooms = request.form["rooms"]
            photo = request.files["photo"]
            photoname = photo.filename
            photo.save("static/images/properties/" + photoname)
            print("here")
            property = Properties(
                Address=address,
                Locality=locality,
                Area=area,
                Price=price,
                Rent=False,
                Date_Of_Construction=yearOfConstruction,
                No_Of_Bedrooms=rooms,
                Status="Available",
                Sell_Date=None,
                Sell_Price=None,
            )
            db.session.add(property)
            db.session.commit()
            property = (
                Properties.query.filter(Properties.Address == address)
                .filter(Properties.Locality == locality)
                .first()
            )
            propertyPhoto = Photos(P_ID=property.P_ID, Photo_URL=photoname)
            sells = Sells(Seller_ID=session["userID"], P_ID=property.P_ID)
            db.session.add(propertyPhoto)
            db.session.commit()
            db.session.add(sells)
            db.session.commit()
            return redirect(url_for("home"))

        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/search", methods=["POST"])
def search():
    min_price = None
    max_price = None
    area = None
    locality = None
    availability = None
    status = None
    localities = Brokers.query.with_entities(Brokers.Locality.distinct()).all()
    areas = Properties.query.with_entities(Properties.Area.distinct()).all()
    if request.method == "POST":
        ret = Properties.query.filter(Properties.Status != "Sold")
        locality = request.form["locality"]
        min_price = request.form["min_price"]
        max_price = request.form["max_price"]
        area = request.form["area"]
        availability = request.form["availability"]
        if locality != "-":
            ret = ret.filter(Properties.Locality == locality)

        if availability != "-":
            if availability == "sale":
                ret = ret.filter(Properties.Rent == 0)
            else:
                ret = ret.filter(Properties.Rent == 1)

        if status != "-":
            if status == "sold":
                ret = ret.filter(Properties.Status == "Sold")
            else:
                ret = ret.filter(Properties.Status != "Sold")

        if area != "-":
            area = area.split("-")
            ret = ret.filter(Properties.Area <= int(area[1])).filter(
                Properties.Area >= int(area[0])
            )
        ret = ret.filter(Properties.Price >= min_price).filter(
            Properties.Price <= max_price
        )

        return render_template(
            "home/index.html",
            properties=ret.join(Photos).all(),
            localities=localities,
            areas=areas,
        )

    else:
        return redirect(url_for("home"))


@app.route("/sold", methods=["GET", "POST"])
def sold():
    if request.method == "GET":
        properties = (
            Properties.query.filter(Properties.Status == "Sold").join(Photos).all()
        )
        localities = Brokers.query.with_entities(Brokers.Locality.distinct()).all()
        areas = Properties.query.with_entities(Properties.Area.distinct()).all()
        min_area = min(areas)[0]
        max_area = max(areas)[0]
        diff = (max_area - min_area) // 6
        areas = list(range(min_area, max_area + 1, diff))
        print(areas)

        if "badlogin" in session.keys():
            session.pop("badlogin")
            flash("Either userID or Password is wrong!")
        return render_template(
            "home/index.html", properties=properties, localities=localities, areas=areas
        )
    else:
        return redirect(url_for("home"))
