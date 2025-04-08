import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def table_exists(table_name):
    """Verifica se uma tabela existe no banco de dados"""
    result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", table_name)
    return len(result) > 0


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if not table_exists("transactions"):
        return apology("Transactions table is missing in the database", 200)

    # Obter ações e saldo
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                      user_id=session["user_id"])[0]["cash"]

    # Calcular valores totais
    total_value = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote:
            stock["name"] = quote["name"]
            stock["price"] = quote["price"]
            stock["value"] = stock["price"] * stock["total_shares"]
            total_value += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer number of shares", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("symbol not found", 400)

        price = quote["price"]
        total_cost = int(shares) * price

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if user_cash < total_cost:
            return apology("not enough cash", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        if table_exists("transactions"):
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                session["user_id"], symbol, shares, price
            )
        else:
            return apology("Transactions table is missing in the database", 00)

        flash(f"Bought {shares} shares of {symbol} for {usd(total_cost)}!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if not table_exists("transactions"):
        return apology("Transactions table is missing in the database", 200)

    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"]
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists", 400)

        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)

        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if not table_exists("transactions"):
        return apology("Transactions table is missing in the database", 200)

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol or not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid symbol and shares", 400)

        shares = int(shares)
        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["total_shares"] < shares:
                    return apology("not enough shares", 400)

                quote = lookup(symbol)
                price = quote["price"]
                total_sale = shares * price

                db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                           total_sale, session["user_id"])
                db.execute(
                    "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                    session["user_id"], symbol, -shares, price
                )
                flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}!")
                return redirect("/")
        return apology("symbol not found", 400)

    return render_template("sell.html", stocks=stocks)
