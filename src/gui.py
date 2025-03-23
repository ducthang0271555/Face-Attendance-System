import tkinter as tk
import cv2
import os
from tkinter import messagebox
import auth



def start_gui():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("400x600")

    def format_dob(event):
        text = entry_dob.get()
        text = ''.join(filter(str.isdigit, text))
        if len(text) > 2:
            text = text[:2] + '/' + text[2:]
        if len(text) > 5:
            text = text[:5] + '/' + text[5:]
        if len(text) > 10:
            text = text[:10]

        entry_dob.delete(0, tk.END)
        entry_dob.insert(0, text)
        entry_dob.icursor(tk.END)

    entry_username = tk.Entry(root)
    entry_password = tk.Entry(root, show="*")
    entry_employee_name = tk.Entry(root)
    employee_code_var = tk.StringVar()
    employee_code_var.set("NV")
    option_employee_code = tk.OptionMenu(root, employee_code_var, "NV", "TP", "GĐ")
    employee_gender = tk.StringVar()
    employee_gender.set("Khác")
    option_employee_gender = tk.OptionMenu(root, employee_gender, "Khác", "Nam", "Nữ")
    entry_dob = tk.Entry(root)
    entry_phone = tk.Entry(root)
    entry_position = tk.Entry(root)
    entry_dob.bind("<KeyRelease>", format_dob)

    def show_initial_ui():
        close_all_btn_label_entry_option()

        btn_login.pack(pady=5)
        btn_attendance.pack(pady=5)

    def capture_image():
        employee_code = employee_code_var.get()  # Lấy mã nhân viên từ dropdown
        if not employee_code:
            messagebox.showerror("Lỗi", "Vui lòng chọn mã nhân viên trước khi chụp ảnh")
            return

        cap = cv2.VideoCapture(0)  # Mở camera

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Chụp ảnh - Nhấn Space để chụp, ESC để thoát", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 32:
                if not os.path.exists("images"):
                    os.makedirs("images")
                image_path = f"images/{employee_code}.jpg"
                cv2.imwrite(image_path, frame)
                messagebox.showinfo("Thành công", f"Ảnh đã được lưu: {image_path}")
                break
            elif key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_login_form():
        close_all_btn_label_entry_option()
        label_username.pack()
        entry_username.pack()
        label_password.pack()
        entry_password.pack()
        btn_login_confirm.pack(pady=5)
        btn_back.pack(pady=5)

    def show_register_form():
        close_all_btn_label_entry_option()

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
        close_all_btn_label_entry_option()
        show_initial_ui()

    def go_back_to_admin_ui():
        close_all_btn_label_entry_option()
        show_admin_ui()

    def show_admin_ui():
        close_all_btn_label_entry_option()

        btn_register_admin.pack(pady=5)
        btn_add_employee.pack(pady=5)
        btn_update_employee.pack(pady=5)
        btn_logout.pack(pady=5)

    def show_add_employee():
        close_all_btn_label_entry_option()

        label_employee_code.pack(pady=5)
        option_employee_code.pack(pady=5)
        label_employee_name.pack(pady=5)
        entry_employee_name.pack(pady=5)
        label_gender.pack(pady=5)
        option_employee_gender.pack(pady=5)
        label_DOB.pack(pady=5)
        entry_dob.pack(pady=5)
        label_phone.pack(pady=5)
        entry_phone.pack(pady=5)
        label_position.pack(pady=5)
        entry_position.pack(pady=5)
        btn_capture_image.pack(pady=5)
        btn_add_employee_confirm.pack(pady=5)
        btn_back_to_admin_ui.pack(pady=5)

    def logout():
        auth.logout()
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        show_initial_ui()

    def close_all_btn_label_entry_option():
        btn_login.pack_forget()
        btn_attendance.pack_forget()
        btn_login_confirm.pack_forget()
        btn_back.pack_forget()
        btn_logout.pack_forget()
        btn_add_employee.pack_forget()
        btn_update_employee.pack_forget()
        btn_register_admin.pack_forget()
        btn_register_confirm.pack_forget()
        btn_back_to_admin_ui.pack_forget()
        btn_add_employee_confirm.pack_forget()
        btn_capture_image.pack_forget()

        label_username.pack_forget()
        label_password.pack_forget()
        label_employee_code.pack_forget()
        label_employee_name.pack_forget()
        label_gender.pack_forget()
        label_DOB.pack_forget()
        label_phone.pack_forget()
        label_position.pack_forget()

        entry_username.pack_forget()
        entry_password.pack_forget()
        entry_employee_name.pack_forget()
        entry_dob.pack_forget()
        entry_phone.pack_forget()
        entry_position.pack_forget()

        option_employee_code.pack_forget()
        option_employee_gender.pack_forget()

    def attendance():
        messagebox.showinfo("Thành công", "Co cai cc, chua lam dau")

    label_username = tk.Label(root, text="Tên đăng nhập:")
    label_password = tk.Label(root, text="Mật khẩu:")
    label_employee_code = tk.Label(root, text="Mã nhân viên:")
    label_employee_name = tk.Label(root, text="Tên nhân viên:")
    label_gender = tk.Label(root, text="Giới tính:")
    label_DOB = tk.Label(root, text="Ngày sinh:")
    label_phone = tk.Label(root, text="Số điện thoại")
    label_position = tk.Label(root, text="Địa chỉ:")

    btn_login = tk.Button(root, text="Đăng nhập", command=show_login_form, width=20, height=2)
    btn_attendance = tk.Button(root, text="Chấm công", command=attendance, width=20, height=2)
    btn_login_confirm = tk.Button(root, text="Xác nhận đăng nhập", command=login_action, width=20, height=2)
    btn_back = tk.Button(root, text="Quay lại", command=go_back, width=20, height=2)
    btn_logout = tk.Button(root, text="Đăng xuất", command=logout, width=20, height=2)
    btn_add_employee = tk.Button(root, text="Thêm nhân viên", command=show_add_employee, width=20, height=2)
    btn_update_employee = tk.Button(root, text="Cập nhật nhân viên", width=20, height=2)
    btn_register_admin = tk.Button(root, text="Đăng ký", command=show_register_form, width=20, height=2)
    btn_register_confirm = tk.Button(root, text="Xác nhận đăng ký", command=register_action, width=20, height=2)
    btn_back_to_admin_ui = tk.Button(root, text="Quay lại", command=go_back_to_admin_ui, width=20, height=2)
    btn_add_employee_confirm = tk.Button(root, text="Thêm nhân viên", width=20, height=2)
    btn_capture_image = tk.Button(root, text="Chụp ảnh", command=capture_image, width=20, height=2)

    show_initial_ui()
    root.mainloop()