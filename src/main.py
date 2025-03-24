from database import initialize_db
from gui import start_gui
import os

def main():
    print("🔹 Khởi tạo cơ sở dữ liệu...")
    initialize_db()

    print("🔹 Mở giao diện...")
    start_gui()

if __name__ == "__main__":
    main()
