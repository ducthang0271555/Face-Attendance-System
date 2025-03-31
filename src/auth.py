import sqlite3
from tkinter import messagebox

is_logged_in = False

def login(username, password):
    global is_logged_in

    with sqlite3.connect("./attendance.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result and password == result[0]:
        is_logged_in = True
        return True
    return False

def register(username, password):
    conn = sqlite3.connect("./attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()