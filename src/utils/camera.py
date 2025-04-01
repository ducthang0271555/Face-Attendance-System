import cv2
import os
import tkinter as tk
from tkinter import messagebox
from src.database import Database

def capture_image(id, code, name):
    if not id or not code or not name:
        return None
    cap = cv2.VideoCapture(0)

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
            image_path = f"images/{code}_{id}_{sanitized_name}.jpg"

            db = Database()
            db.save_img_of_employee(id, image_path)

            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Chúc mừng", "Bạn đã thêm thành công nhân viên!")

            cap.release()
            cv2.destroyAllWindows()
            return image_path

        elif key == 27:  # Nhấn ESC để thoát
            db = Database()
            db.cancel_employee(id)
            break
    cap.release()
    cv2.destroyAllWindows()
    return None

def update_image(id, code, name):
    if not id or not code or not name:
        return None

    cap = cv2.VideoCapture(0)

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
            image_path = f"images/{code}_{id}_{sanitized_name}_temp.jpg"
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Chúc mừng", "Bạn đã chụp thành công!")
            cap.release()
            cv2.destroyAllWindows()
            return image_path
        elif key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return None