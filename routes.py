from app import app
from flask import render_template, request, redirect, session, flash
import users
import restaurants


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
            return redirect("/")
        else:
            flash("Restaurant already exists")
            return redirect("/newrestaurant")
