import unittest
from datetime import date
from employee_mgmt import EmployeeManagementSystem

class TestEmployeeManagementSystemLevel4(unittest.TestCase):
    def setUp(self):
        self.ems = EmployeeManagementSystem()
        self.ems.create_department(1, "Sales")
        self.ems.create_department(2, "IT")
        self.ems.create_employee(1, "John Doe", "Manager", 1, date(2022, 1, 1), "john@example.com", "1234567890", 50.00, 4.5)
        self.ems.create_employee(2, "Jane Smith", "Engineer", 2, date(2022, 2, 1), "jane@example.com", "9876543210", 60.00, 4.2)
        self.ems.create_employee(3, "Mike Johnson", "Analyst", 1, date(2022, 3, 1), "mike@example.com", "5678901234", 45.00, 4.8)
        self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)
        self.ems.record_timesheet(2, 1, date(2023, 6, 2), 7)
        self.ems.record_timesheet(3, 2, date(2023, 6, 1), 9)
        self.ems.record_timesheet(4, 2, date(2023, 6, 2), 6)
        self.ems.record_timesheet(5, 3, date(2023, 6, 1), 8)
        self.ems.record_timesheet(6, 3, date(2023, 6, 2), 7)

    def test_create_department(self):
        self.ems.create_department(3, "Finance")
        department = self.ems.get_department(3)
        self.assertEqual(department.name, "Finance")

    def test_transfer_employee(self):
        self.ems.transfer_employee(1, 2)
        employee = self.ems.get_employee(1)
        self.assertEqual(employee.department_id, 2)
        transfer_history = self.ems.get_employee_transfer_history(1)
        self.assertEqual(len(transfer_history), 1)
        self.assertEqual(transfer_history[0].previous_department_id, 1)
        self.assertEqual(transfer_history[0].new_department_id, 2)

    def test_calculate_department_salary_expenditure(self):
        self.ems.create_payroll(1, 1, date(2023, 6, 1), date(2023, 6, 15))
        self.ems.create_payroll(2, 3, date(2023, 6, 1), date(2023, 6, 15))
        expenditure = self.ems.calculate_department_salary_expenditure(1, date(2023, 6, 1), date(2023, 6, 30))
        self.assertEqual(expenditure, 1140.00)

    def test_get_top_performing_employees(self):
        top_employees = self.ems.get_top_performing_employees(1, 1)
        self.assertEqual(len(top_employees), 1)
        self.assertEqual(top_employees[0].employee_id, 3)

if __name__ == '__main__':
    unittest.main()