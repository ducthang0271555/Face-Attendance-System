import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
from auth import login, register
from database import Database
from utils.camera import capture_image, update_image
from PIL import Image, ImageTk
import cv2
import os
from deepface import DeepFace
import time
import sqlite3
from datetime import datetime
import pandas as pd

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Chấm Công")
        self.root.geometry("900x800")

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
    
    def ghi_diem_danh(self,ten):
        conn = sqlite3.connect("./attendance.db")
        cursor = conn.cursor()
        ngay = datetime.now().strftime("%Y-%m-%d")

        # Lấy tất cả lượt điểm danh hôm nay của người đó
        cursor.execute("""
            SELECT * FROM diem_danh
            WHERE ten = ? AND DATE(thoi_gian) = ?
            ORDER BY thoi_gian ASC
        """, (ten, ngay))
        cac_lan_diem_danh = cursor.fetchall()

        if len(cac_lan_diem_danh) == 0:
            loai = "vao"
        elif len(cac_lan_diem_danh) == 1:
            loai = "ra"
        else:
            print(f"⚠️ {ten} đã điểm danh đủ 2 lần hôm nay.")
            conn.close()
            return

        thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO diem_danh (ten, thoi_gian, loai)
            VALUES (?, ?, ?)
        """, (ten, thoi_gian, loai))
        conn.commit()
        conn.close()

        print(f"✅ Ghi điểm danh: {ten} - {loai.upper()} lúc {thoi_gian}")

    def attendance(self):
        start_time = time.time()
        camera_on_duration = 15
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        thu_muc_anh_mau = "images"
        nguong_distance = 0.3  # Tùy chỉnh ngưỡng so sánh
        xac_thuc_thanh_cong = False

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Nhan dien khuon mat (Nhan ESC de thoat)", frame)
            if time.time() - start_time > camera_on_duration:
                messagebox.showerror("Lỗi,Không phát hiện khuôn mặt")
                break
            # Chuyển sang ảnh xám để detect khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                cv2.imwrite("temp_frame.jpg", frame)

                # Duyệt qua tất cả ảnh trong thư mục
                for ten_file in os.listdir(thu_muc_anh_mau):
                    duong_dan_anh_mau = os.path.join(thu_muc_anh_mau, ten_file)

                    try:
                        result = DeepFace.verify(
                            "temp_frame.jpg",
                            duong_dan_anh_mau,
                            model_name="Facenet512",
                            enforce_detection=False
                        )

                        if result["verified"] and result["distance"] < nguong_distance:
                            # lấy tên nv từ path images
                            s = os.path.splitext(ten_file)[0]
                            parts = s.split("_")
                            full_name = " ".join(parts[2:])
                            print(f"✅ Xác thực thành công: {full_name}")
                            print("Khoảng cách:", result["distance"])
                            self.ghi_diem_danh(full_name)
                            xac_thuc_thanh_cong = True
                            # Hiển thị tên người lên camera
                            cv2.putText(frame, f"Xac thuc: {full_name}", (20, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.imshow("Nhan dien khuon mat", frame)
                            cv2.waitKey(3000)
                            break
                        

                    except Exception as e:
                        print(f"Lỗi với ảnh {ten_file}: {e}")
                        continue

            if xac_thuc_thanh_cong:
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def xuat_excel(self,theo_ngay=None, theo_thang=None):
        conn = sqlite3.connect("attendance.db")
        query = "SELECT ten, thoi_gian, loai FROM diem_danh"
        df = pd.read_sql_query(query, conn)
        conn.close()

        df["thoi_gian"] = pd.to_datetime(df["thoi_gian"])

        if theo_ngay:
            try:
                ngay = pd.to_datetime(theo_ngay)
                df = df[df["thoi_gian"].dt.date == ngay.date()]
                file_name = f"diem_danh_ngay_{ngay.strftime('%Y_%m_%d')}.xlsx"
            except:
                messagebox.showerror("Lỗi", "Ngày không hợp lệ (YYYY-MM-DD)")
                return

        elif theo_thang:
            try:
                thang = pd.to_datetime(theo_thang + "-01")
                df = df[(df["thoi_gian"].dt.month == thang.month) & (df["thoi_gian"].dt.year == thang.year)]
                file_name = f"diem_danh_thang_{thang.strftime('%Y_%m')}.xlsx"
            except:
                messagebox.showerror("Lỗi", "Tháng không hợp lệ (YYYY-MM)")
                return
        else:
            file_name = "diem_danh_toan_bo.xlsx"

        df = df.sort_values(by=["thoi_gian"])
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Thành công", f"Đã xuất: {file_name}")
        # ✅ Tự động mở file Excel
        try:
            os.startfile(file_name)  # Windows
        except AttributeError:
            try:
                import subprocess
                subprocess.call(["open", file_name])  # macOS
            except:
                subprocess.call(["xdg-open", file_name])  # Linux
    def tao_giao_dien_bao_cao_cong(self):
        root = tk.Tk()
        root.title("Xuất Excel điểm danh")

        tk.Label(root, text="Ngày (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        entry_ngay = tk.Entry(root, width=20)
        entry_ngay.grid(row=0, column=1)

        tk.Label(root, text="Tháng (YYYY-MM):").grid(row=1, column=0, padx=10, pady=5)
        entry_thang = tk.Entry(root, width=20)
        entry_thang.grid(row=1, column=1)

        def xuat():
            ngay = entry_ngay.get().strip()
            thang = entry_thang.get().strip()
            
            self.xuat_excel(theo_ngay=ngay if ngay else None,
                    theo_thang=thang if thang else None)

        tk.Button(root, text="Xuất Excel", command=xuat, bg="green", fg="white", padx=10).grid(row=2, columnspan=2, pady=10)

        root.mainloop()
    def lay_du_lieu(self,theo_ngay=None, theo_thang=None):
        conn = sqlite3.connect("attendance.db")
        query = "SELECT ten, thoi_gian, loai FROM diem_danh"
        df = pd.read_sql_query(query, conn)
        conn.close()

        df["thoi_gian"] = pd.to_datetime(df["thoi_gian"])

        if theo_ngay:
            try:
                ngay = pd.to_datetime(theo_ngay)
                df = df[df["thoi_gian"].dt.date == ngay.date()]
            except:
                messagebox.showerror("Lỗi", "Ngày không hợp lệ (YYYY-MM-DD)")
                return pd.DataFrame()

        elif theo_thang:
            try:
                thang = pd.to_datetime(theo_thang + "-01")
                df = df[(df["thoi_gian"].dt.month == thang.month) & (df["thoi_gian"].dt.year == thang.year)]
            except:
                messagebox.showerror("Lỗi", "Tháng không hợp lệ (YYYY-MM)")
                return pd.DataFrame()

        df = df.sort_values(by="thoi_gian")
        return df
    def tao_giao_dien_lich_su(self):
        root = tk.Tk()
        root.title("🕒 Lịch sử điểm danh")

        # Entry nhập ngày
        tk.Label(root, text="Ngày (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_ngay = tk.Entry(root)
        entry_ngay.grid(row=0, column=1, padx=5)

        # Entry nhập tháng
        tk.Label(root, text="Tháng (YYYY-MM):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_thang = tk.Entry(root)
        entry_thang.grid(row=1, column=1, padx=5)

        # Bảng Treeview hiển thị dữ liệu
        cols = ("ten", "thoi_gian", "loai")
        tree = ttk.Treeview(root, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Hàm xử lý khi bấm "Hiển thị"
        def hien_thi():
            for row in tree.get_children():
                tree.delete(row)

            ngay = entry_ngay.get().strip()
            thang = entry_thang.get().strip()
            df = self.lay_du_lieu(theo_ngay=ngay if ngay else None,
                            theo_thang=thang if thang else None)

            for _, row in df.iterrows():
                tree.insert("", "end", values=(row["ten"], row["thoi_gian"], row["loai"]))

        tk.Button(root, text="Hiển thị", command=hien_thi, bg="blue", fg="white", padx=10).grid(row=2, column=0, columnspan=2, pady=5)

        root.mainloop()

    def show_manager_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Button(self.main_frame, text="Đăng ký", command= lambda: self.show_register_form(), width=20, height=2).pack(pady=15)
        tk.Button(self.main_frame, text="Thêm nhân viên", command= lambda: self.show_add_employee(), width=20, height=2).pack(pady=15)
        tk.Button(self.main_frame, text="Danh sách nhân viên", command= lambda: self.show_employee_list(), width=20, height=2).pack(pady=15)
        tk.Button(self.main_frame, text="Xuất báo cáo chấm công", command= lambda: self.tao_giao_dien_bao_cao_cong(), width=20, height=2).pack(pady=15)
        tk.Button(self.main_frame, text="Lịch sử chấm công", command= lambda: self.tao_giao_dien_lich_su(), width=20, height=2).pack(pady=15)
        tk.Button(self.main_frame, text="Đăng xuất", width=20, height=2, command=self.logout).pack(pady=15)


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

    def show_employee_list(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Danh sách nhân viên", font=("Arial", 14)).pack(pady=10)

        columns = ("ID", "Mã NV", "Tên", "Giới tính", "Ngày sinh", "SĐT", "Địa chỉ", "Ảnh")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        db = Database()
        employees = db.get_all_employees()

        for emp in employees:
            self.tree.insert("", "end", values=emp)

        self.tree.bind("<Double-1>", self.on_employee_select)

        tk.Button(self.main_frame, text="Quay Lại", command=self.show_manager_ui).pack(pady=10)

    def on_employee_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        emp_data = item["values"]

        self.show_edit_employee(emp_data)

    def show_edit_employee(self, emp_data):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        emp_id, employee_code, name, gender, dob, phone, address, image_path, *_ = emp_data

        self.new_image_path = image_path
        self.img_origin = image_path

        tk.Label(self.main_frame, text="Cập nhật nhân viên", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.main_frame, text="Mã nhân viên:").pack(pady=5)
        self.employee_code_var = tk.StringVar(value=employee_code)
        tk.OptionMenu(self.main_frame, self.employee_code_var, "NV", "TP", "GD").pack(pady=5)

        tk.Label(self.main_frame, text="Tên:").pack()
        name_entry = tk.Entry(self.main_frame)
        name_entry.insert(0, name)
        name_entry.pack()

        tk.Label(self.main_frame, text="Giới tính:").pack()
        gender_var = tk.StringVar(value=gender)
        tk.OptionMenu(self.main_frame, gender_var, "Nam", "Nữ", "Khác").pack()

        tk.Label(self.main_frame, text="Ngày sinh:").pack(pady=5)
        self.dob_entry = tk.Entry(self.main_frame)
        self.dob_entry.insert(0, dob)
        self.dob_entry.pack(pady=5)
        self.dob_entry.bind("<KeyRelease>", self.format_dob)

        tk.Label(self.main_frame, text="Số điện thoại:").pack()
        phone_entry = tk.Entry(self.main_frame)
        phone_entry.insert(0, phone)
        phone_entry.pack()

        tk.Label(self.main_frame, text="Địa chỉ:").pack()
        address_entry = tk.Entry(self.main_frame)
        address_entry.insert(0, address)
        address_entry.pack()

        self.img_label = tk.Label(self.main_frame)
        self.img_label.pack(pady=5)

        # Hiển thị ảnh nếu có
        if self.new_image_path:
            try:
                img = Image.open(self.new_image_path)
                img = img.resize((150, 150))  # Resize ảnh về 150x150
                self.photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=self.photo)
            except Exception as e:
                print(f"Lỗi mở ảnh: {e}")
                tk.Label(self.main_frame, text="Không thể hiển thị ảnh").pack(pady=5)

        def update_new_image(emp_id, employee_code, name_entry):
            img_path_temp = update_image(emp_id, employee_code, name_entry)
            if img_path_temp:
                self.new_image_path = img_path_temp
                try:
                    img = Image.open(self.new_image_path)
                    img = img.resize((150, 150))
                    self.photo = ImageTk.PhotoImage(img)
                    self.img_label.config(image=self.photo)  # Cập nhật ảnh trong Label
                except Exception as e:
                    print(f"Lỗi mở ảnh mới: {e}")
                    tk.Label(self.main_frame, text="Không thể hiển thị ảnh mới").pack(pady=5)

        tk.Button(self.main_frame, text="Chụp lại ảnh",
                  command=lambda: update_new_image(emp_id, employee_code, name_entry.get())).pack(pady=5)

        tk.Button(self.main_frame, text="Lưu", command=lambda: self.update_employee(
            emp_id, self.employee_code_var.get(), name_entry.get(), gender_var.get(), self.dob_entry.get(),
            phone_entry.get(), address_entry.get(), self.new_image_path)
                  ).pack(pady=5)

        tk.Button(self.main_frame, text="Xóa", command=lambda: self.delete_employee(emp_id)).pack(pady=5)
        tk.Button(self.main_frame, text="Quay Lại", command=self.show_employee_list).pack(pady=5)

    def update_employee(self, emp_id, employee_code, name, gender, dob, phone, address, img_path):
        # Lưu lại ảnh tạm
        img_temp = img_path
        img_old = img_path

        sanitized_name = name.replace(" ", "_")
        new_img_path = f"images/{employee_code}_{emp_id}_{sanitized_name}.jpg"

        if img_old != new_img_path:
            try:
                os.rename(img_old, new_img_path)
                img_path = new_img_path
            except Exception as e:
                t = 1


        if img_path and '_temp' in img_path:
            if img_temp and os.path.exists(img_temp):
                # Lấy tên file gốc (không có _temp)
                original_img_path = img_temp.replace('_temp', '')  # Xóa _temp trong tên file

                # Xóa ảnh cũ (nếu có)
                if os.path.exists(original_img_path):
                    os.remove(original_img_path)

                # Di chuyển ảnh mới từ ảnh tạm và bỏ _temp
                shutil.move(img_temp, original_img_path)  # Di chuyển và đổi tên ảnh

                # Cập nhật thông tin nhân viên trong cơ sở dữ liệu
                db = Database()
                db.update_employee(emp_id, employee_code, name, gender, dob, phone, address, original_img_path)

                messagebox.showinfo("Thành công", "Nhân viên đã được cập nhật!")
            else:
                messagebox.showerror("Lỗi", "Đường dẫn ảnh không hợp lệ!")
        else:
            if self.img_origin and os.path.exists(self.img_origin):
                os.remove(self.img_origin)

            db = Database()
            db.update_employee(emp_id, employee_code, name, gender, dob, phone, address, img_path)

            messagebox.showinfo("Thành công", "Nhân viên đã được cập nhật!")
        self.show_employee_list()

    def delete_employee(self, emp_id):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?")
        if confirm:
            db = Database()
            db.delete_employee(emp_id)
            messagebox.showinfo("Thành công", "Nhân viên đã bị xóa!")
            self.show_employee_list()