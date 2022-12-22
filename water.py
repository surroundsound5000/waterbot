import sqlite3
import time 
from gpiozero import LED

# Using the predefined class LED instead of Output Device as it requires less defining
pump = LED(17)

times = {
    5 : '5:00',
    6 : '6:00',
    7 : '7:00',
    8 : '8:00'
}

days = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday" 
}

def get_db_connection():
    conn = sqlite3.connect('waterbot.db')
    conn.row_factory = sqlite3.Row
    return conn

def load_db():
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM schedule').fetchall()
    conn.close()
    return schedule

def select_day(current_day,sched):
    '''Iterates through sched then returns the row matching the current day'''

    for i in range(7):
        if days[current_day] == sched[i][1]:
            return sched[i]

def hoursleep():
    '''Sleeps until the next hour kicks over'''
    now = time.localtime()
    time.sleep((59-now[4])*60+(60-now[5]))
    return

def monitor():
    while True:
        schedule = load_db()
        now = time.localtime()
        today = select_day(now[6],schedule)
        if today[2] == "YES":
            try:
                if today[3] == times[now[3]]:
                    pump.on()
                    time.sleep(today[4]*60)
                    pump.off()
            except:
                pass
        hoursleep()

if __name__=='__main__':
    pump.off()
    monitor()