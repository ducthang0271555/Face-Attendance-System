# Face-Attendance-System
face_attendance/
│── src/
│   │── main.py                # File chính để chạy ứng dụng
│   │── gui.py                 # Giao diện người dùng (Tkinter)
│   │── auth.py                # Xác thực đăng nhập (nếu có)
│   │── face_recognition.py     # Nhận diện khuôn mặt
│   │── database.py             # Xử lý cơ sở dữ liệu
│   │── attendance.py           # Xử lý logic chấm công
│   ├── models/
│   │   ├── employee.py         # Lớp đại diện cho nhân viên
│   │   ├── attendance_record.py# Lớp đại diện cho bản ghi chấm công
│   ├── utils/
│   │   ├── camera.py           # Xử lý camera
│   │   ├── image_processing.py # Tiền xử lý ảnh
│   ├── assets/                 # Chứa ảnh hoặc dữ liệu huấn luyện
│── .python-version             # Phiên bản Python sử dụng
│── attendance.db               # Cơ sở dữ liệu SQLite
│── requirements.txt            # Các thư viện cần thiết
│── README.md                   # Hướng dẫn sử dụng
