import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import time 

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

# Create available times
times = ['5:00','6:00','7:00','8:00']
runtimes = [1,2,3,5,7,10,15,20,30]

''' Routes a'hoy!'''

@app.route('/', methods=["GET", "POST"])
def index():

    # Script for updating database
    if request.method == "POST":
        start = time.time()
        # Update database based on checkboxes
        conn = get_db_connection()
        schedule = conn.execute('SELECT * FROM schedule').fetchall()
        for day in schedule:
            print(request.form.get(day['day']),"@", time.time()-start)
            if request.form.get(day['day']):
                conn.execute('''UPDATE schedule SET active = 'YES' WHERE day = ? ''', [day['day']])
            else:
                conn.execute('''UPDATE schedule SET active = 'NO' WHERE day = ? ''', [day['day']])
            conn.execute('''UPDATE schedule SET time = ? WHERE day = ? ''', (request.form.get('time'+day['day']), day['day']))
            conn.execute('''UPDATE schedule SET runtime = ? WHERE day = ? ''', (request.form.get('runtime'+day['day']), day['day']))
        conn.commit()
        schedule = conn.execute('SELECT * FROM schedule').fetchall()
        conn.close()
        print("Update complete @ ", time.time()-start)
        return render_template('index.html', schedule = schedule, times=times, runtimes=runtimes)


   # Load index page (assuming no update)
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM schedule').fetchall()
    conn.close()  
    return render_template('index.html', schedule = schedule, times=times, runtimes=runtimes)
    
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
        conn = get_db_connection()
        users = conn.execute('''SELECT * FROM users WHERE username = ?''', [request.form.get("username")]).fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return render_template('login.html', error="Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='192.168.15.37')
    
