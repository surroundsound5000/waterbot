import sqlite3
import time 

def get_db_connection():
    conn = sqlite3.connect('waterbot.db')
    conn.row_factory = sqlite3.Row
    return conn

def do_watering():
    for i in range(10):  
        print(time.localtime())
        time.sleep(1)
    exit()

if __name__=='__main__':
    do_watering()