import frappe
import random
import string
from frappe.utils.password import update_password

@frappe.whitelist()
def create_users_with_passwords():
  

    def generate_password(length=10):
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choices(characters, k=length))

    created_users = []
    employees = frappe.get_all("Employee", fields=["name", "employee_name","company_email","cell_number"],filters=[["status","=", "Active"], ["user_id", "is", "not set"]])
    for employee in employees:

        # Generate a random password
        password = generate_password()

        if not frappe.db.exists("User", employee.company_email):
            # Create User
            user = frappe.get_doc({
                "doctype": "User",
                "email": employee.company_email,
                "first_name": employee.employee_name,
                "user_type": "Website User",
                "send_welcome_email": 0,
                "enabled": 1
            })
            user.insert(ignore_permissions=True)
        else:
            user = frappe.get_doc("User", employee.company_email)

        # Set password
        update_password(user.name, password)

        # Link to employee
        emp = frappe.get_doc("Employee", employee.name)
        emp.user_id = user.name
        emp.save(ignore_permissions=True)
        

        created_users.append({
            "employee": employee.name,
            "email": employee.company_email,
            "password": password,
            "mobile": employee.cell_number
        })

    frappe.db.commit()
    return created_users
