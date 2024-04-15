import unittest
from datetime import date
from employee_mgmt import EmployeeManagementSystem

class TestEmployeeManagementSystemLevel1(unittest.TestCase):
    def setUp(self):
        self.ems = EmployeeManagementSystem()

    def test_create_employee(self):
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1))
        employee = self.ems.get_employee(1)
        self.assertEqual(employee.name, "John Doe")
        self.assertEqual(employee.job_title, "Manager")
        self.assertEqual(employee.department, "Sales")
        self.assertEqual(employee.start_date, date(2022, 1, 1))

    def test_create_employee_duplicate_id(self):
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1))
        with self.assertRaises(Exception):
            self.ems.create_employee(1, "Jane Smith", "Engineer", "IT", date(2022, 2, 1))

    # def test_create_employee_invalid_data(self):
    #     with self.assertRaises(ValueError):
    #         self.ems.create_employee(1, 123, "Manager", "Sales", date(2022, 1, 1))
    #     with self.assertRaises(ValueError):
    #         self.ems.create_employee(1, "John Doe", "Manager", "Sales", "2022-01-01")

    def test_record_timesheet(self):
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1))
        self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)
        timesheet = self.ems.get_timesheet(1)
        self.assertEqual(timesheet.employee_id, 1)
        self.assertEqual(timesheet.date, date(2023, 6, 1))
        self.assertEqual(timesheet.hours_worked, 8)

    def test_record_timesheet_duplicate_id(self):
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1))
        self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)
        with self.assertRaises(Exception):
            self.ems.record_timesheet(1, 1, date(2023, 6, 2), 7)

    def test_record_timesheet_invalid_employee(self):
        with self.assertRaises(Exception):
            self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)

    # def test_record_timesheet_invalid_data(self):
    #     self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1))
    #     with self.assertRaises(ValueError):
    #         self.ems.record_timesheet("invalid", 1, date(2023, 6, 1), 8)
    #     with self.assertRaises(ValueError):
    #         self.ems.record_timesheet(1, 1, "2023-06-01", 8)
    #     with self.assertRaises(ValueError):
    #         self.ems.record_timesheet(1, 1, date(2023, 6, 1), "8")

if __name__ == '__main__':
    unittest.main()