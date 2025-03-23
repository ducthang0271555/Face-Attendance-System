# Face-Attendance-System

```
1. Quản lý nhân viên
 - Thêm, sửa, xóa thông tin nhân viên (ID, họ tên, phòng ban, chức vụ, v.v.).

 - Lưu trữ hình ảnh khuôn mặt nhân viên để nhận diện.

 - Xuất danh sách nhân viên ra file CSV/Excel.

2. Nhận diện khuôn mặt & Chấm công
 - Mở camera để quét khuôn mặt nhân viên.

 - So sánh khuôn mặt với dữ liệu đã lưu.

 - Ghi nhận thời gian điểm danh (giờ vào, giờ ra).

 - Lưu thông tin chấm công vào cơ sở dữ liệu.

 - Hiển thị trạng thái điểm danh (Thành công / Thất bại / Khuôn mặt không xác định).

3. Quản lý chấm công
 - Xem lịch sử chấm công của nhân viên.

 - Xuất báo cáo chấm công ra file CSV/Excel.

 - Tìm kiếm và lọc dữ liệu theo ngày, tháng, nhân viên.

4. Giao diện người dùng (Desktop App - Tkinter)
Màn hình chính với các chức năng chính.

 - Giao diện quản lý nhân viên.

 - Giao diện hiển thị camera và kết quả nhận diện.

 - Giao diện báo cáo chấm công.

5. Bảo mật & Quyền hạn
 - Đăng nhập cho quản trị viên.

 - Phân quyền (Quản trị viên có thể thêm/xóa nhân viên, nhân viên chỉ có thể xem thông tin cá nhân).

 - Lưu nhật ký hệ thống để theo dõi hoạt động.
```

```
CẤU TRÚC THAM KHẢO

face_attendance/
│── src/
│   │── main.py                # File chính để chạy ứng dụng
│   │── gui.py                 # Giao diện người dùng (Tkinter)
│   │── auth.py                 # Xác thực đăng nhập (nếu có)
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
```

