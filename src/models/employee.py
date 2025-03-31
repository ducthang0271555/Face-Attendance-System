from database import Database

class Employee:
    def __init__(self, employee_code, name, gender, dob, phone, address, image_path):
        self.employee_code = employee_code
        self.name = name
        self.gender = gender
        self.dob = dob
        self.phone = phone
        self.address = address
        self.image_path = image_path

