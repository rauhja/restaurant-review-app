from app import app
from flask import render_template, request, redirect, session, flash
import users
import restaurants
import reviews


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            flash("Incorrect username or password")
            return redirect("/login")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            flash("Passwords do not match")
            return redirect("/signup")
        if users.signup(username, password):
            return redirect("/")
        else:
            flash("Username already taken")
            return redirect("/signup")

@app.route("/newrestaurant", methods=["GET", "POST"])
def addrestaurant():
    if request.method == "GET":
        return render_template("newrestaurant.html")
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        postnumber = request.form["postnumber"]
        city = request.form["city"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        website = request.form["website"]
        if restaurants.add(name, address, postnumber, city, latitude, longitude, website):
            return redirect("/newrestaurant")
        else:
            flash("Restaurant already exists")
            return redirect("/newrestaurant")

@app.route("/restaurants")
def listrestaurants():
    return render_template("restaurants.html", restaurants=restaurants.list())

@app.route("/restaurants/<int:id>")
def restaurant(id):
    return render_template("restaurant.html", restaurant=restaurants.get(id), reviews=reviews.getreview(id))

@app.route("/send", methods=["POST"])
def sendreview():
    restaurant_id = request.form["restaurant_id"]
    review = request.form["review"]
    rating = request.form["rating"]
    if reviews.addreview(restaurant_id, review, rating):
        return redirect("/restaurants/" + restaurant_id)
    else:
        flash("Error")
        return redirect("/")

@app.route("/deletereview/<restaurant_id>/<int:id>")
def deletereview(id, restaurant_id):
    if reviews.deletereview(id):
        return redirect("/restaurants/" + restaurant_id)
    else:
        flash("Error")
        return redirect("/")