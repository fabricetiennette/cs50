from database import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

import datetime

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    # query for cash
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    
    # cash in USD
    total_cash = usd(cash[0]["cash"])
    
    # list of lists declaration for rendering
    final_portfolio = []
    
    # variable declaration of total of stock prices sum
    total_stock = 0.0
    
    # try to access portfolio table
    try:
        # query for portfolio
        portfolio = db.execute("SELECT sum(share), symbol FROM portfolio WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])
        
        # for each stock create a new list for indexing
        for stock in portfolio:
        
            # create a new list with stock info in this order
            new_list = []
        
            # symbol lookup
            symbol = lookup(stock['symbol'])
        
            # 1. Symbol append
            new_list.append(stock.get("symbol"))
        
            # 2. Name append
            new_list.append(symbol.get("name"))
        
            # 3. Sum of shares append
            new_list.append(stock.get("sum(share)"))
        
            # 4. Price in usd append
            new_list.append(usd(symbol.get("price")))
        
            # 5. Total of price * shares
            total = symbol.get("price")*stock.get("sum(share)")
        
            new_list.append(usd(total))
        
            # add this stock total to total of stocks
            total_stock += total
        
            # append whole list to final_portfolio list
            final_portfolio.append(new_list)
    
    except RuntimeError:
            pass
    
    
    # usd format function call    
    total_stock = usd(total_stock)

    return render_template("index.html", total_cash=total_cash, portfolio=final_portfolio, total_stock=total_stock)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("invalid symbol")
            
        elif not request.form.get("shares") or not request.form.get("shares").isdigit():
            return apology("invalid shares")
            
        # get users input from form
        quote_request = request.form.get("symbol")
        
        # query yahoo for quote
        quote = lookup(quote_request)
    
        if not quote:
            return apology("invalid symbol")
        
        # query for cash amount    
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        
        # total shares bought
        total = quote.get("price")*int(request.form.get("shares"))
        
        # check if user has enough cash
        if total > cash[0]["cash"]:
            return apology("can't afford")
        else:
            cash[0]["cash"] -= total
            
        # time object with now datetime for portfolio table
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # access portfolio table, if don't exist create new tables
        try:
            # query to select new table
            db.execute("SELECT share, symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
            
                
        except RuntimeError :
            # create history transaction table
            db.execute("CREATE TABLE history (symbol TEXT, share INTEGER, price INTEGER, date TEXT UNIQUE, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id) )")
            
            # create portfolio table
            db.execute("CREATE TABLE portfolio (symbol TEXT, share INTEGER, user_id INTEGER)")
        
        # update cash balance    
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash[0]["cash"], user_id=session["user_id"])
        
        # insert transaction into history table        
        db.execute("INSERT INTO history ( symbol, share, price, date, user_id ) VALUES (:symbol, :share, :price, :date, :user_id )", symbol=quote.get("symbol"),share=request.form.get("shares"),price=quote.get("price"),date=date,user_id=session["user_id"])    
        
        sum_share = db.execute("SELECT sum(share) FROM portfolio WHERE user_id = :user_id AND symbol=:symbol", user_id=session["user_id"],symbol=quote.get("symbol"))
        
        if sum_share[0]["sum(share)"] == None:
            db.execute("INSERT INTO portfolio (symbol, share, user_id) VALUES(:symbol, :share, :user_id)", user_id=session["user_id"], symbol=quote.get("symbol"), share=request.form.get("shares"))
        else:
            
            if sum_share[0]["sum(share)"] == None:
                new_share = int(request.form.get("shares"))
            else:
                new_share = sum_share[0]["sum(share)"] + int(request.form.get("shares"))

            # insert stock into portfolio table
            db.execute("UPDATE portfolio SET share=:share WHERE user_id = :user_id AND symbol = :symbol", symbol=quote.get("symbol"),share=new_share,user_id=session["user_id"])
        
        
        flash("Bought!")
        
        return redirect(url_for("index"))
      
      
      
      
@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    # list of lists declaration for rendering
    final_portfolio = []
    
    # variable declaration of total of stock prices sum
    total_stock = 0.0
    
    # try to access portfolio table
    try:
        # query for portfolio
        portfolio = db.execute("SELECT symbol, share, price, date FROM history WHERE user_id = :user_id ORDER BY date", user_id=session["user_id"])
        
        # for each stock create a new list for indexing
        for stock in portfolio:
        
            # create a new list with stock info in this order
            new_list = []
        
            # symbol lookup
            symbol = lookup(stock['symbol'])
        
            # 1. Symbol append
            new_list.append(stock.get("symbol"))

            # 2. Shares append
            new_list.append(stock.get("share"))
        
            # 4. Price in usd append
            new_list.append(usd(stock.get("price")))
        
            # 5. Date append
            new_list.append(stock.get("date"))
        
            # append whole list to final_portfolio list
            final_portfolio.append(new_list)
    
    except RuntimeError:
            pass
        
        
    return render_template("history.html", history=final_portfolio)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
       
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        
        # get users input from form
        quote_request = request.form.get("symbol")
        
        # query yahoo for quote
        quote = lookup(quote_request)
    
        if not quote:
            return apology("invalid symbol")
        else:
            return render_template("quoted.html", share=quote.get("name"), symbol=quote.get("symbol"), price=usd(quote.get("price"))) 


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        # ensure password-confirmation was submitted   
        elif not request.form.get("password-confirmation"):
            return apology("password (again)")
        
        # ensure password was confirmed
        elif not request.form.get("password") == request.form.get("password-confirmation"):
            return apology("please confirm password")
     
        # query database for username
        results = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        # create password hash
        hash = pwd_context.encrypt(request.form.get("password"))
        
        # ensure username exists else adds new user
        if results:
            return apology("username unavailable")
        else:
            # insert new user and password to users table
            new_user = db.execute("INSERT INTO users (username,hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
            
            # new query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            
            # remember which user has logged in
            session["user_id"] = rows[0]["id"]
            
            #
            flash("Registered!")
            
            # redirect new user to home page
            return redirect(url_for("index"))
            

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    if request.method == "GET":
        return render_template("sell.html")
    elif request.method == "POST":
        
        # check for valid input
        if not request.form.get("symbol"):
            return apology("invalid symbol")
            
        elif not request.form.get("shares") or not request.form.get("shares").isdigit():
            return apology("invalid shares")
            
        # get users input from form
        quote_request = request.form.get("symbol")
        
        # query yahoo for quote
        quote = lookup(quote_request)
    
        # if symbol is not valid
        if not quote:
            return apology("invalid symbol")
            
        # query for cash balance
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # query for shares amount, try to find the symbol if not return apologize
        try:
            shares = db.execute("SELECT symbol, share FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=quote.get("symbol"))
            
        except RuntimeError :
            return apologize("symbol not owned")
            
        # total of shares user wants to sale
        total = int(request.form.get("shares"))
        
        # check if user has enough shares
        if total > int(shares[0]["share"]):
            return apology("can't afford")
     
        else:
            cash[0]["cash"] = total*quote.get("price")
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash[0]["cash"], user_id=session["user_id"])
            
            total = shares[0]["share"] - total
            
            if total == 0:
                db.execute("DELETE FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=quote.get("symbol"))
            else:
                db.execute("UPDATE portfolio SET share = :total WHERE user_id = :user_id AND symbol = :symbol", total=total, user_id=session["user_id"], symbol=quote.get("symbol"))
        

        flash("Sold!")  
            
        return redirect(url_for("index"))
        
        
        
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("old_pwd"):
            return apology("must provide password")

        # ensure password was submitted
        elif not request.form.get("new_pwd"):
            return apology("must provide new password")
            
        # ensure password-confirmation was submitted   
        elif not request.form.get("confirm_pwd"):
            return apology("please confirm password")
        
        # ensure password was confirmed
        elif not request.form.get("new_pwd") == request.form.get("confirm_pwd"):
            return apology("please confirm new password")
     
        # query database for password hash
        results = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])
        
        # ensure password is correct
        if len(results) != 1 or not pwd_context.verify(request.form.get("old_pwd"), results[0]["hash"]):
            return apology("invalid password")
        
        # create password hash
        hash = pwd_context.encrypt(request.form.get("new_pwd"))
        
       
        # insert new user and password to users table
        new_user = db.execute("UPDATE users SET hash =:hash WHERE id = :id", id=session["user_id"], hash=hash)
            
        # 
        flash("Password changed")
            
        # redirect new user to home page
        return redirect(url_for("index"))
            

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("account.html")