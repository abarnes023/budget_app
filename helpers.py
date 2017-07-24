from cs50 import SQL
from flask import redirect, request, session, url_for
from functools import wraps

# configure to use SQLite database
db = SQL("sqlite:///budget.db")

# requires a user to be logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("landing", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# check database to see if data for selected month exists    
def budget_data(month):
    data = db.execute("SELECT * FROM 'budgets' WHERE user = :user AND month = :month", user=session["user_id"], month=month)
    if len(data) > 0:
            # pull values from database
            e_income = data[0]["e_income"]
            a_income = data[0]["a_income"]
            e_rent = data[0]["e_rent"]
            a_rent = data[0]["a_rent"]
            e_util = data[0]["e_util"]
            a_util = data[0]["a_util"]
            e_food = data[0]["e_food"]
            a_food = data[0]["a_food"]
            e_ent = data[0]["e_ent"]
            a_ent = data[0]["a_ent"]
            e_save = data[0]["e_save"]
            a_save = data[0]["a_save"]
            
    else:
            # set variables to None
            e_income = None
            a_income = None
            e_rent = None
            a_rent = None
            e_util = None
            a_util = None
            e_food = None
            a_food = None
            e_ent = None
            a_ent = None
            e_save = None
            a_save = None
            
    return {'e_income': e_income, 'a_income': a_income, 'e_rent': e_rent, 'a_rent': a_rent, 'e_util': e_util, 'a_util': a_util, 'e_food': e_food, 'a_food': a_food, 'e_ent': e_ent, 'a_ent': a_ent, 'e_save': e_save, 'a_save': a_save}

# Formats value as USD
def usd(value):
    return "${:,.2f}".format(value)