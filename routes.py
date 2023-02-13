from app import app
from flask import render_template, request, redirect, session, flash
import users
import restaurants
import reviews
import tags

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
        if len(username) < 3:
            flash("Username must be at least 3 characters long")
            return redirect("/signup")
        password = request.form["password"]
        if len(password) < 6:
            flash("Password must be at least 6 characters long")
            return redirect("/signup")
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
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        postnumber = request.form["postnumber"]
        city = request.form["city"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        website = request.form["website"]
        restaurant_tags = request.form.getlist("tags")
        if restaurants.getid(name, address):
            flash("Restaurant already exists")
            return redirect("/newrestaurant")
        if restaurants.add(name, address, postnumber, city, latitude, longitude, website):
            for tag in restaurant_tags:
                id = restaurants.getid(name, address)
                tags.addtagtorestaurant(id[0], tag)
            return redirect("/restaurants")
        else:
            flash("Error")
            return redirect("/newrestaurant")
    return render_template("newrestaurant.html")

@app.route("/restaurants")
def listrestaurants():
    return render_template("restaurants.html", restaurants=restaurants.listall())

@app.route("/restaurants/<int:id>")
def restaurant(id):
    return render_template("restaurant.html", restaurant=restaurants.get(id), reviews=reviews.getreview(id), score=reviews.getscore(id), tags=tags.getrestauranttag(id))

@app.route("/deleterestaurant/<int:id>")
def deleterestaurant(id):
    if restaurants.delete(id):
        return redirect("/restaurants")
    else:
        flash("Error")
        return redirect("/")

@app.route("/send", methods=["POST"])
def sendreview():
    restaurant_id = request.form["restaurant_id"]
    review = request.form["review"]
    if review == "":
        flash("Please write a review")
        return redirect("/restaurants/" + restaurant_id)
    if len(review) > 255:
        flash("Review must be less than 255 characters")
        return redirect("/restaurants/" + restaurant_id)
    if "rating" not in request.form:
        flash("Please rate the restaurant")
        return redirect("/restaurants/" + restaurant_id)
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
    
@app.route("/result")
def result():
    return render_template("restaurants.html", restaurants=restaurants.search(request.args["query"]))

@app.route("/searchbytag")
def searchbytag():
    return render_template("restaurants.html", restaurants=restaurants.searchbytag(request.args["type"]))