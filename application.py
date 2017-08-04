from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from flask_session import Session
from flask_jsglue import JSGlue
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime
import feedparser
from helpers import *

# configure application
app = Flask(__name__)
JSGlue(app)

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
    
    username = get_user()
    return render_template("index.html", username=username)
    
@app.route("/about")
@login_required
def about():
    ### Display the about us page. """
    
    username = get_user()
    return render_template("about.html", username=username)
    
@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    ### Allows user to create budget. """
    
    # get username
    username = get_user()
    
    # if reached via POST
    if request.method == "POST":
        # set selected month
        currMonth = request.form.get("month")
        if not currMonth:
            flash("Must enter month")
            return redirect(url_for("budget"))
        
        # get variables from form
        e_income = request.form.get("e_income")
        a_income = request.form.get("a_income")
        e_rent = request.form.get("e_rent")
        a_rent = request.form.get("a_rent")
        e_util = request.form.get("e_util")
        a_util = request.form.get("a_util")
        e_food = request.form.get("e_food")
        a_food = request.form.get("a_food")
        e_ent = request.form.get("e_ent")
        a_ent = request.form.get("a_ent")
        e_save = request.form.get("e_save")
        a_save = request.form.get("a_save")
            
        # check database to see if data for selected month exists
        data = db.execute("SELECT * FROM 'budgets' WHERE user = :user AND month = :month", user=session["user_id"], month=currMonth)
        if len(data) > 0:
            # update values in database
            db.execute("""UPDATE 'budgets'
                        SET e_income = :e_income, a_income = :a_income, e_rent = :e_rent, a_rent = :a_rent, e_util = :e_util, a_util = :a_util, e_food = :e_food, a_food = :a_food, e_ent = :e_ent, a_ent = :a_ent, e_save = :e_save, a_save = :a_save
                        WHERE user = :user AND month = :month""", e_income=e_income, a_income=a_income, e_rent=e_rent, a_rent=a_rent, e_util=e_util, a_util=a_util, e_food=e_food, a_food=a_food, e_ent=e_ent, a_ent=a_ent, e_save=e_save, a_save=a_save, user=session["user_id"], month=currMonth)
        else:
            # insert values into database
            db.execute("""INSERT INTO 'budgets'
                        (user, month, e_income, a_income, e_rent, a_rent, e_util, a_util, e_food, a_food, e_ent, a_ent, e_save, a_save) VALUES (:user, :month, :e_income, :a_income, :e_rent, :a_rent, :e_util, :a_util, :e_food, :a_food, :e_ent, :a_ent, :e_save, :a_save)""",
                        user=session["user_id"], month=currMonth, e_income=e_income, a_income=a_income, e_rent=e_rent, a_rent=a_rent, e_util=e_util, a_util=a_util, e_food=e_food, a_food=a_food, e_ent=e_ent, a_ent=a_ent, e_save=e_save, a_save=a_save)
        
        # check percent saved and spent on rent
        rent = spending(a_rent, a_income)
        saved = spending(a_save, a_income)
        
        return render_template("budget.html", username=username, currMonth=currMonth, e_income=e_income, a_income=a_income, e_rent=e_rent, a_rent=a_rent, e_util=e_util, a_util=a_util, e_food=e_food, a_food=a_food, e_ent=e_ent, a_ent=a_ent, e_save=e_save, a_save=a_save, rent=rent, saved=saved)
    
    # if reached via GET
    else:
        # get current month and year
        currMonth = datetime.now().strftime("%Y-%m")
        
        # pull month's data from database
        data = budget_data(currMonth)
        
        # check percent saved and spent on rent
        rent = spending(data['a_rent'], data['a_income'])
        saved = spending(data['a_save'], data['a_income'])
        
        return render_template("budget.html", username=username, currMonth=currMonth, e_income=data['e_income'], a_income=data['a_income'], e_rent=data['e_rent'], a_rent=data['a_rent'], e_util=data['e_util'], a_util=data['a_util'], e_food=data['e_food'], a_food=data['a_food'], e_ent=data['e_ent'], a_ent=data['a_ent'], e_save=data['e_save'], a_save=data['a_save'], rent=rent, saved=saved)

@app.route("/month")
def month():
    """Pulls current month data when month is changed"""
    
    # get month entered by user - if no month entered default to current month
    month = request.args.get("month", datetime.now().strftime("%Y-%m"))
    
    # get budget data for month as a dictionary
    data = budget_data(month)
    
    return json.dumps(data)

@app.route("/articles")
def articles():
    """Display last 10 articles from Get Rich Slowly blog"""
    
    # Parse through RSS feed of Get Rich Slowly
    feed = feedparser.parse("http://www.getrichslowly.org/blog/feed/")
    
    # Get current username
    username = get_user()
    
    return render_template("articles.html", username=username, feed=feed)
    
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash("You have successfully been logged out.", "success")
    return redirect(url_for("login"))