from database import initialize_db
from gui import start_gui

def main():
    print("🔹 Khởi tạo cơ sở dữ liệu...")
    initialize_db()

    print("🔹 Mở giao diện...")
    start_gui()  # Chạy giao diện từ gui.py

if __name__ == "__main__":
    main()
