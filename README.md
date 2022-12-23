# Waterbot
#### Video Demo: https://youtu.be/yKN7U_4wO8U
#### Github Repo: https://github.com/surroundsound5000/waterbot
#### Description:
The goal is to make an automated watering pump. But with a web app running on a Raspberry Pi that controls the pump. 


# Steps Involved
## Pi
  Just flash a regular Raspbian image to a regular RasPi.
## Flask
  Install Flask on the RasPi. Couldn't do this on the work network because security. Once you're on a regular network its pretty straightforward.
  Had to do it again in codespaces (allowing me to work on the project while at work) using 
  `pip3 install -r requirements.txtpip3 install -r requirements.txt`
  Also updated the flask version requirement (and relevant dependencies) to allow use of `flask --debug run`
  
## Git
  Get github working on the RasPi. Need to use SSH for pushes/ commits, which means generating a new key on the pi and registering this GitHub. 
## Website
  Build a basic website - I used Bootstrap pretty heavily. I basically didn't use any other CSS or JS, just what bootstrap provides (this involved a handful of workarounds but seems fine).
## Python
  I have never used python with GPIO so this should be interesting.
## SQL
  I'm using a SQLite3 database to keep track of when the pi should be watering. 

  Set up with 

  `CREATE TABLE schedule (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, day TEXT NOT NULL, active  TEXT NOT NULL, time DATETIME, runtime DATETIME);` 

  and populated with 

  `INSERT INTO schedule (day, active) VALUES ('Monday', 'YES');` 
  etc. 

Then used flask and Jinja to dynamically populate the table with 

`@app.route('/')
def index():
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM schedule').fetchall()
    conn.close()
    return render_template('index.html', schedule = schedule)`

in the / route and 

```{% for day in schedule %}
<tr>
  <td>
    {{ day['day'] }}
  </td>
  <td>
    {% if day['active'] == 'YES' %}
      <i class="bi bi-check-square"></i>
    {% else %}
      <i class="bi bi-square"></i>
    {% endif %}
  </td>
  <td>
    {{ day['time'] }}
  </td>
  <td>
    {{ day['time'] }}
  </td>
</tr>
{% endfor %}
```  
in index.html.

## Login
  Also using SQLite3 to keep track of administrative accounts. 
  Used the python code:
  
`from werkzeug.security import generate_password_hash
print(generate_password_hash("Password.1"))`

to generate a hash, then stored it in a users table in the database by opening `sqlite3 waterbot.db` and running:

`CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);`

to create the table, then

`insert into users (username, hash) values ("user", "260000$zzb1quTYPkgqIi9h$de4a80cbc64a4c97ba31aa36f97de3358797128854c66e2c248218f368e4733d");`

to store the user account. 

Test credentials include *user: password* and *username: pass*.

## The watering part!

Within app.py, I have used os.fork() to allow the web app to create an instance of the watering script, which will monitor the database and manage the actual watering. 
  
  This allows the web server to continue doing it's thing while the watering app (water.py) keeps doing its job as well. 

