import sqlite3


class Database:
    def __init__(self, db_name="attendance.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
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
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS managers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        self.conn.commit()

    def save_employee(self, employee_code, name, gender, dob, phone, address):
        self.cursor.execute("""
        INSERT INTO employees (employee_code, name, gender, dob, phone, address) VALUES (?, ?, ?, ?, ?, ?)
        """, (employee_code, name, gender, dob, phone, address))

        employee_id = self.cursor.lastrowid

        self.conn.commit()
        return employee_id

    def cancel_employee(self, employee_id):
        self.cursor.execute("""
        DELETE FROM employees WHERE id = ?""", (employee_id,))

        self.conn.commit()

    def save_img_of_employee(self, employee_id, image_path):
        self.cursor.execute("""
                    UPDATE employees
                    SET image_path = ?
                    WHERE id = ?
                """, (image_path, employee_id))

        self.conn.commit()

    def get_all_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()