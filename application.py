from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure to use SQLite database
db = SQL("sqlite:///budget.db")

# landing page
@app.route("/landing")
def landing():
    """ Direct site visitor to landing page. """
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register a new user. """
    
    # if user reached via POST
    if request.method == "POST":
        
        # ensure unique username entered
        if not request.form.get("username"):
            flash("Please enter a username.", "error")
            return redirect(url_for("register"))
        duplicates = db.execute("SELECT * FROM 'users' WHERE username = :username", username=request.form.get("username"))
        if len(duplicates) > 0:
            flash("Username is already taken.", "error")
            return redirect(url_for("register"))
        
        # ensure passwords entered match
        if not request.form.get("password") or not request.form.get("password2"):
            flash("Please enter and re-enter a password.", "error")
            return redirect(url_for("register"))
        if request.form.get("password") != request.form.get("password2"):
            flash("Passwords don't match.", "error")
            return redirect(url_for("register"))
            
        # insert user into database
        user_id = db.execute("INSERT INTO 'users' (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))
        
        # store user id
        session["user_id"] = user_id
        
        # redirect to home page
        flash("You have successfully been registered.", "success")
        return redirect(url_for("index"))
        
    # if reached route via GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in the user. """
    
    # forget any logged in user
    session.clear()
    
    # if user reached via POST
    if request.method == "POST":
        
        # ensure credentials entered
        if not request.form.get("username"):
            flash("Please enter a username.", "error")
            return redirect(url_for("login"))
        elif not request.form.get("password"):
            flash("Please enter a password.", "error")
            return redirect(url_for("login"))
        
        # query database to check for user
        rows = db.execute("SELECT * FROM 'users' WHERE username = :username", username=request.form.get("username"))
        
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("Username or password is incorrect.", "error")
            return redirect(url_for("login"))
        
        # remember user if login valid
        session["user_id"] = rows[0]["id"]
        
        # redirect to home page
        flash("You have successfully been logged in.", "success")
        return redirect(url_for("index"))
        
    # if reached via GET
    else:
        return render_template("login.html")
        
# home page
@app.route("/")
@login_required
def index():
    ### Displays user homepage. """
    
    user = db.execute("SELECT username FROM 'users' WHERE id = :id", id=session["user_id"])
    username = user[0]["username"]
    return render_template("index.html", username=username)
    
@app.route("/about")
@login_required
def about():
    ### Display the about us page. """
    
    user = db.execute("SELECT username FROM 'users' WHERE id = :id", id=session["user_id"])
    username = user[0]["username"]
    return render_template("about.html", username=username)
    
@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    ### Allows user to create budget. """
    
    user = db.execute("SELECT username FROM 'users' WHERE id = :id", id=session["user_id"])
    username = user[0]["username"]
    
    # if reached via POST
    if request.method == "POST":
        
        # get variables from form and set to 0 if None
        e_income = if_none(request.form.get("e_income"))
        a_income = if_none(request.form.get("a_income"))
        e_rent = if_none(request.form.get("e_rent"))
        a_rent = if_none(request.form.get("a_rent"))
        e_util = if_none(request.form.get("e_util"))
        a_util = if_none(request.form.get("a_util"))
        e_food = if_none(request.form.get("e_food"))
        a_food = if_none(request.form.get("a_food"))
        e_ent = if_none(request.form.get("e_ent"))
        a_ent = if_none(request.form.get("a_ent"))
        e_save = if_none(request.form.get("e_save"))
        a_save = if_none(request.form.get("a_save"))
        
        
    
        return render_template("budget.html", username=username)
    
    # if reached via GET
    else:
        return render_template("budget.html", username=username)
    
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash("You have successfully been logged out.", "success")
    return redirect(url_for("login"))
    
# check if variable is None
def if_none(v):
    if not v:
        v = 0
        return v
    else:
        return v