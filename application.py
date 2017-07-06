from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
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

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

# home page
@app.route("/")
@login_required
def index():
    
    # TODO
    
    return render_template("index.html")

# landing page
@app.route("/landing")
def landing():
    """ Direct site visitor to landing page. """
    render_template("landing.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in the user. """
    
    # forget any logged in user
    session.clear()
    
    # if user reached via POST
    if request.method == "POST":
        
        # ensure credentials entered
        if request.form.get("username")