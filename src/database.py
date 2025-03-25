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
            employee_code TEXT NOT NULL,
            name TEXT NOT NULL,
            gender TEXT CHECK( gender IN ('Nam', 'Nữ', 'Khác') ) NOT NULL,
            dob DATE,
            phone TEXT,
            address TEXT,
            image_path TEXT,
            join_date DATE DEFAULT CURRENT_DATE
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

def save_employee(employee_code, name, gender, dob, phone, address):
    conn = sqlite3.connect("./attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO employees (employee_code, name, gender, dob, phone, address) VALUES (?, ?, ?, ?, ?, ?)
    """, (employee_code, name, gender, dob, phone, address))

    employee_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return employee_id

def cancel_employee(employee_id):
    conn = sqlite3.connect("./attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM employees WHERE id = ?""",(employee_id,))

    conn.commit()
    conn.close()

def save_img_of_employee(employee_id, image_path):
    conn = sqlite3.connect("./attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE employees
            SET image_path = ?
            WHERE id = ?
        """, (image_path, employee_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
