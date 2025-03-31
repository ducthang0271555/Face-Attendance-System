import cv2
import os
import tkinter as tk
from tkinter import messagebox

from src.database import save_img_of_employee, cancel_employee


def capture_image(employee_code, name, employee_id, entry_employee_name, entry_dob, entry_phone, entry_address):
    if not employee_code or not name or not employee_id:
        messagebox.showerror("Lỗi", "Thiếu thông tin nhân viên, vui lòng kiểm tra lại!")
        return None

    cap = cv2.VideoCapture(0)  # Mở camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Chụp ảnh - Nhấn Space để chụp, ESC để thoát", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Nhấn Space để chụp ảnh
            if not os.path.exists("images"):
                os.makedirs("images")

            sanitized_name = name.replace(" ", "_")
            image_path = f"images/{employee_code}_{sanitized_name}_{employee_id}.jpg"

            save_img_of_employee(employee_id, image_path)

            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Chúc mừng", "Bạn đã thêm thành công nhân viên!")

            # Xóa trắng form sau khi thêm thành công
            entry_employee_name.delete(0, tk.END)
            entry_dob.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            entry_address.delete(0, tk.END)

            cap.release()
            cv2.destroyAllWindows()
            return image_path

        elif key == 27:  # Nhấn ESC để thoát
            cancel_employee(employee_id)
            break

    cap.release()
    cv2.destroyAllWindows()
    return None