from database import Database
from gui import AttendanceApp
import tkinter as tk

if __name__ == "__main__":
    db = Database()
    db.close()

    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
