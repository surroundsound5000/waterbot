import sqlite3
from flask import Flask, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash

app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Link the database to the Flask app
def get_db_connection():
    conn = sqlite3.connect('waterbot.db')
    conn.row_factory = sqlite3.Row
    return conn


''' Routes a'hoy!'''

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('login.html', error="Must provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('login.html', error="Must provide password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template('login.html', error="Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='192.168.15.37')
    
