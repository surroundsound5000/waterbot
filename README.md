# Waterbot
#### Video Demo:  <URL HERE>
#### Description:
The goal is to make an automated watering pump. But with a web server running on a Raspberry Pi that controls the pump. 

## Steps involved
### Pi
  Just flash a regular Raspbian image to a regular RasPi.
### Flask
  Install Flask on the RasPi. Couldn't do this on the work network because security. Once you're on a regular network its pretty straightforward. 
### Git
  Get github working on the RasPi. Need to use SSH for pushes/ commits, which means generating a new key on the pi and registering this GitHub. 
### Website
  Build a basic website - I used Bootstrap pretty heavily. I am keen to try to complete the task with no other CSS or Javascript - we'll see how long my patience lasts.
### Python
  I have never used python with GPIO so this should be interesting.
### SQL
  Will use a SQL database to keep track of when the pi should be watering. 
