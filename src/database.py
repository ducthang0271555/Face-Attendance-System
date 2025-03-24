import sqlite3

def initialize_db():
    conn = sqlite3.connect("./attendance.db")
    cursor = conn.cursor()

    # Tạo bảng user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tạo bảng nhân viên
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT CHECK( gender IN ('Nam', 'Nữ', 'Khác') ) NOT NULL,
            dob DATE,
            phone TEXT UNIQUE,
            address TEXT,
            position TEXT,
            join_date DATE DEFAULT CURRENT_DATE,
            image_path TEXT NOT NULL
        )
    """)

    # Tạo bảng chấm công
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            date DATE NOT NULL,
            check_in DATETIME,
            check_out DATETIME,
            status TEXT CHECK( status IN ('Đúng giờ', 'Đi muộn', 'Về sớm', 'Nghỉ') ),
            note TEXT,
            FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_db()
