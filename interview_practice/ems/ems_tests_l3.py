import unittest
from datetime import date
from employee_mgmt import EmployeeManagementSystem

class TestEmployeeManagementSystemLevel3(unittest.TestCase):
    def setUp(self):
        self.ems = EmployeeManagementSystem()
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1), "john@example.com", "1234567890", 50.00)
        self.ems.create_employee(2, "Jane Smith", "Engineer", "IT", date(2022, 2, 1), "jane@example.com", "9876543210", 60.00)
        self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)
        self.ems.record_timesheet(2, 1, date(2023, 6, 2), 7)
        self.ems.record_timesheet(3, 2, date(2023, 6, 1), 9)
        self.ems.record_timesheet(4, 2, date(2023, 6, 2), 6)

    def test_create_payroll(self):
        self.ems.create_payroll(1, 1, date(2023, 6, 1), date(2023, 6, 15))
        payroll = self.ems.get_payroll_by_id(1)
        self.assertEqual(payroll.employee_id, 1)
        self.assertEqual(payroll.total_hours, 15)
        self.assertEqual(payroll.gross_pay, 750.00)
        self.assertEqual(payroll.net_pay, 600.00)

    def test_get_employee_payrolls(self):
        self.ems.create_payroll(1, 1, date(2023, 6, 1), date(2023, 6, 15))
        self.ems.create_payroll(2, 1, date(2023, 6, 16), date(2023, 6, 30))
        payrolls = self.ems.get_employee_payrolls(1)
        self.assertEqual(len(payrolls), 2)
        self.assertEqual(payrolls[0].payroll_id, 1)
        self.assertEqual(payrolls[1].payroll_id, 2)

    def test_update_employee_details(self):
        self.ems.update_employee_details(1, email="johndoe@example.com", phone_number="5551234567", hourly_rate=55.00)
        employee = self.ems.get_employee(1)
        self.assertEqual(employee.email, "johndoe@example.com")
        self.assertEqual(employee.phone_number, "5551234567")
        self.assertEqual(employee.hourly_rate, 55.00)

    def test_calculate_employee_salary(self):
        self.ems.create_payroll(1, 1, date(2023, 6, 1), date(2023, 6, 15))
        self.ems.create_payroll(2, 1, date(2023, 6, 16), date(2023, 6, 30))
        salary = self.ems.calculate_employee_salary(1, date(2023, 6, 1), date(2023, 7, 1))
        self.assertEqual(salary, 600.00)

    def test_promote_employee(self):
        self.ems.promote_employee(1, "Senior Manager", 10.00)
        employee = self.ems.get_employee(1)
        self.assertEqual(employee.job_title, "Senior Manager")
        self.assertEqual(employee.hourly_rate, 60.00)

if __name__ == '__main__':
    unittest.main()