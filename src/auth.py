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
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        is_logged_in = True
        return True  # Đăng nhập thành công
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
        return False  # Đăng nhập thất bại

def logout():
    global is_logged_in
    is_logged_in = False
    messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất!")

def register(username, password):
    if not username or not password:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
        return

    conn = sqlite3.connect("../attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Thành công", "Đăng ký thành công!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")

    conn.close()
