# Waterbot
#### Video Demo:  <URL HERE>
#### Description:
The goal is to make an automated watering pump. But with a web server running on a Raspberry Pi that controls the pump. 

## Steps Involved
### Pi
  Just flash a regular Raspbian image to a regular RasPi.
### Flask
  Install Flask on the RasPi. Couldn't do this on the work network because security. Once you're on a regular network its pretty straightforward.
  Had to do it again in codespaces (allowing me to work on the project while at work) using 
  `pip3 install -r requirements.txtpip3 install -r requirements.txt`
  Also updated the flask version requirement (and relevant dependencies) to allow use of `flask --debug run`
  
### Git
  Get github working on the RasPi. Need to use SSH for pushes/ commits, which means generating a new key on the pi and registering this GitHub. 
### Website
  Build a basic website - I used Bootstrap pretty heavily. I am keen to try to complete the task with no other CSS or Javascript - we'll see how long my patience lasts.
### Python
  I have never used python with GPIO so this should be interesting.
### SQL
  Will use a SQL database to keep track of when the pi should be watering. 
### Login
  Also using SQLite3 to keep track of administrative accounts. 
  Used the python code:
  
`from werkzeug.security import generate_password_hash
print(generate_password_hash("Password.1"))`

to generate a hash, then stored it in a users table in the database by opening `sqlite3 waterbot.db` and running:

`CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);`

to create the table, then

`insert into users (username, hash) values ("user", "260000$zzb1quTYPkgqIi9h$de4a80cbc64a4c97ba31aa36f97de3358797128854c66e2c248218f368e4733d");`

to store the user account. 