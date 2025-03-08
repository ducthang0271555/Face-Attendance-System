import tkinter as tk
from tkinter import messagebox

import auth

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x500")

entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")

def show_initial_ui():
    btn_login.pack(pady=5)
    btn_attendance.pack(pady=5)

    entry_username.pack_forget()
    entry_password.pack_forget()
    btn_login_confirm.pack_forget()
    btn_back.pack_forget()
    btn_logout.pack_forget()
    btn_add_employee.pack_forget()
    btn_update_employee.pack_forget()
    btn_register_admin.pack_forget()

def show_login_form():
    btn_login.pack_forget()
    btn_attendance.pack_forget()
    label_username.pack()
    entry_username.pack()
    label_password.pack()
    entry_password.pack()
    btn_login_confirm.pack(pady=5)
    btn_back.pack(pady=5)

def show_register_form():
    btn_register_admin.pack_forget()
    btn_add_employee.pack_forget()
    btn_update_employee.pack_forget()
    btn_logout.pack_forget()

    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    label_username.pack(pady=5)
    entry_username.pack(pady=5)
    label_password.pack(pady=5)
    entry_password.pack(pady=5)
    btn_register_confirm.pack(pady=5)
    btn_back_to_admin_ui.pack(pady=5)

def login_action():
    username = entry_username.get()
    password = entry_password.get()

    if auth.login(username, password):  # Gọi hàm login từ auth.py
        show_admin_ui()

def register_action():
    username_register = entry_username.get()
    password_register = entry_password.get()
    auth.register(username_register, password_register)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)


def go_back():
    label_username.pack_forget()
    label_password.pack_forget()
    entry_username.pack_forget()
    entry_password.pack_forget()
    btn_back.pack_forget()
    btn_login_confirm.pack_forget()
    show_initial_ui()

def go_back_to_admin_ui():
    entry_username.pack_forget()
    entry_password.pack_forget()
    label_username.pack_forget()
    entry_password.pack_forget()
    btn_register_confirm.pack_forget()
    btn_back_to_admin_ui.pack_forget()

    show_admin_ui()

def show_admin_ui():
    btn_login.pack_forget()
    btn_attendance.pack_forget()
    btn_login_confirm.pack_forget()
    btn_back.pack_forget()
    label_username.pack_forget()
    label_password.pack_forget()
    entry_username.pack_forget()
    entry_password.pack_forget()

    btn_register_admin.pack(pady=5)
    btn_add_employee.pack(pady=5)
    btn_update_employee.pack(pady=5)
    btn_logout.pack(pady=5)

def logout():
    auth.logout()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    show_initial_ui()

def attendance():
    messagebox.showinfo("Thành công", "Co cai cc, chua lam dau")

label_username = tk.Label(root, text="Tên đăng nhập:")
label_password = tk.Label(root, text="Mật khẩu:")

btn_login = tk.Button(root, text="Đăng nhập", command=show_login_form, width=20, height=2)
btn_attendance = tk.Button(root, text="Chấm công",command=attendance, width=20, height=2)
btn_login_confirm = tk.Button(root, text="Xác nhận đăng nhập", command=login_action, width=20, height=2)
btn_back = tk.Button(root, text="Quay lại", command=go_back, width=20, height=2)
btn_logout = tk.Button(root, text="Đăng xuất", command=logout, width=20, height=2)
btn_add_employee = tk.Button(root, text="Thêm nhân viên", width=20, height=2)
btn_update_employee = tk.Button(root, text="Cập nhật nhân viên", width=20, height=2)
btn_register_admin = tk.Button(root, text="Đăng ký", command=show_register_form, width=20, height=2)
btn_register_confirm = tk.Button(root, text="Xác nhận đăng ký",command=register_action, width=20, height=2)
btn_back_to_admin_ui = tk.Button(root, text="Quay lại", command=go_back_to_admin_ui, width=20, height=2)


show_initial_ui()

root.mainloop()
