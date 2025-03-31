import tkinter as tk
from tkinter import messagebox
from auth import login, register
from database import Database
from src.utils.camera import capture_image


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Chấm Công")
        self.root.geometry("300x500")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.login_button = tk.Button(self.main_frame, text="Đăng Nhập", command=self.show_login_form, width=15,
                                      height=2)
        self.login_button.pack(pady=20)
        self.attendance_button = tk.Button(self.main_frame, text="Chấm Công", command=self.attendance, width=15,
                                           height=2)
        self.attendance_button.pack(pady=10)

    def show_login_form(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Tên đăng nhập:").pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Đăng Nhập", command=lambda: self.login()).pack(pady=10)
        tk.Button(self.main_frame, text="Quay Lại", command=self.show_main_buttons).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login(username, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.show_manager_ui()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    def logout(self):
        global is_logged_in
        is_logged_in = False
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất thành công!")
        self.show_main_buttons()

    def attendance(self):
        messagebox.showerror("Hehe", "Co cai cc")

    def show_manager_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Button(self.main_frame, text="Đăng ký", command= lambda: self.show_register_form(), width=15, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Thêm nhân viên", command= lambda: self.show_add_employee(), width=15, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Danh sách nhân viên", width=15, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Đăng xuất", width=15, height=2, command=self.logout).pack(pady=10)


    def show_main_buttons(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.login_button = tk.Button(self.main_frame, text="Đăng Nhập", command=self.show_login_form, width=15,
                                      height=2)
        self.login_button.pack(pady=20)

        self.attendance_button = tk.Button(self.main_frame, text="Chấm Công", command=self.attendance, width=15,
                                           height=2)
        self.attendance_button.pack(pady=10)

    def show_register_form(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Tên đăng nhập:").pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Đăng ký", command= self.register_manager).pack(pady=10)
        tk.Button(self.main_frame, text="Quay Lại", command=self.show_manager_ui).pack(pady=5)

    def show_add_employee(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Mã nhân viên:").pack(pady=5)
        self.employee_code_var = tk.StringVar(value="NV")
        tk.OptionMenu(self.main_frame, self.employee_code_var, "NV", "TP", "GD").pack(pady=5)

        tk.Label(self.main_frame, text="Tên:").pack(pady=5)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Giới tính:").pack(pady=5)
        self.gender_var = tk.StringVar(value="Khác")
        tk.OptionMenu(self.main_frame, self.gender_var, "Nam", "Nữ", "Khác").pack(pady=5)

        tk.Label(self.main_frame, text="Ngày sinh:").pack(pady=5)
        self.dob_entry = tk.Entry(self.main_frame)
        self.dob_entry.pack(pady=5)
        self.dob_entry.bind("<KeyRelease>", self.format_dob)

        tk.Label(self.main_frame, text="Số điện thoại:").pack(pady=5)
        self.phone_entry = tk.Entry(self.main_frame)
        self.phone_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Địa chỉ:").pack(pady=5)
        self.address_entry = tk.Entry(self.main_frame)
        self.address_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Thêm nhân viên", command=self.save_and_capture).pack(pady=10)
        tk.Button(self.main_frame, text="Quay Lại", command=self.show_manager_ui).pack(pady=5)

    def format_dob(self, event):
        text = self.dob_entry.get()
        text = ''.join(filter(str.isdigit, text))
        if len(text) > 2:
            text = text[:2] + '/' + text[2:]
        if len(text) > 5:
            text = text[:5] + '/' + text[5:]
        if len(text) > 10:
            text = text[:10]

        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, text)
        self.dob_entry.icursor(tk.END)

    def register_manager(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
            return

        if register(username, password):
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            return
        messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")

    def save_and_capture(self):
        employee_code = self.employee_code_var.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not dob or not phone or not address:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin nhân viên.")
            return

        db = Database()
        employee_id = db.save_employee(employee_code, name, gender, dob, phone, address)

        confirm = messagebox.askokcancel("Thành công", "Thêm nhân viên thành công, tiến hành chụp ảnh nhân viên?")
        if confirm:
            capture_image(employee_id, employee_code, name)
        else:
            db.cancel_employee(employee_id)




