import unittest
import json
import csv
from datetime import date
from employee_mgmt import EmployeeManagementSystem
from collections import Counter

class TestEmployeeManagementSystemLevel2(unittest.TestCase):
    def setUp(self):
        self.ems = EmployeeManagementSystem()
        self.ems.create_employee(1, "John Doe", "Manager", "Sales", date(2022, 1, 1), "john@example.com", "1234567890", 4.5)
        self.ems.create_employee(2, "Jane Smith", "Engineer", "IT", date(2022, 2, 1), "jane@example.com", "9876543210", 4.2)
        self.ems.create_employee(3, "Mike Johnson", "Manager", "Sales", date(2022, 3, 1), "mike@example.com", "5678901234", 4.8)
        self.ems.record_timesheet(1, 1, date(2023, 6, 1), 8)
        self.ems.record_timesheet(2, 1, date(2023, 6, 2), 7)
        self.ems.record_timesheet(3, 2, date(2023, 6, 1), 9)
        self.ems.record_timesheet(4, 2, date(2023, 6, 2), 6)
        self.ems.record_timesheet(5, 3, date(2023, 6, 1), 8)

    def test_calculate_total_hours(self):
        total_hours = self.ems.calculate_total_hours(1, date(2023, 6, 1), date(2023, 6, 3))
        self.assertEqual(total_hours, 15)

    def test_calculate_total_hours_no_timesheets(self):
        total_hours = self.ems.calculate_total_hours(1, date(2023, 6, 3), date(2023, 6, 4))
        self.assertEqual(total_hours, 0)

    def test_calculate_total_hours_invalid_employee(self):
        with self.assertRaises(Exception):
            self.ems.calculate_total_hours(4, date(2023, 6, 1), date(2023, 6, 2))

    def test_get_employees_by_job_title(self):
        managers = self.ems.get_employees_by_job_title("Manager")
        self.assertEqual(len(managers), 2)
        self.assertIn("John Doe", [manager.name for manager in managers])
        self.assertIn("Mike Johnson", [manager.name for manager in managers])

    def test_get_employees_by_department(self):
        sales_employees = self.ems.get_employees_by_department("Sales")
        self.assertEqual(len(sales_employees), 2)
        self.assertIn("John Doe", [employee.name for employee in sales_employees])
        self.assertIn("Mike Johnson", [employee.name for employee in sales_employees])

    def test_calculate_average_performance_rating(self):
        average_rating = self.ems.calculate_average_performance_rating("Sales")
        self.assertAlmostEqual(average_rating, 4.65)

    def test_calculate_average_performance_rating_no_ratings(self):
        self.ems.create_employee(4, "Amy Brown", "Analyst", "Finance", date(2022, 4, 1), "amy@example.com", "4567890123")
        average_rating = self.ems.calculate_average_performance_rating("Finance")
        self.assertIsNone(average_rating)

    def test_get_top_performers(self):
        top_performers = self.ems.get_top_performers(2)
        self.assertEqual(len(top_performers), 2)
        self.assertIn("Mike Johnson", [employee.name for employee in top_performers])
        self.assertIn("John Doe", [employee.name for employee in top_performers])

    def test_filter_employees_by_start_date(self):
        filtered_employees = self.ems.filter_employees_by_start_date(date(2022, 2, 1))
        self.assertEqual(len(filtered_employees), 2)
        self.assertIn("Jane Smith", [employee.name for employee in filtered_employees])
        self.assertIn("Mike Johnson", [employee.name for employee in filtered_employees])

    def test_export_employee_data_to_json(self):
        exported_data = self.ems.export_employee_data_to_json()
        parsed_data = json.loads(exported_data)
        self.assertEqual(len(parsed_data), 3)
        self.assertIn("John Doe", [employee["name"] for employee in parsed_data])
        self.assertIn("Jane Smith", [employee["name"] for employee in parsed_data])
        self.assertIn("Mike Johnson", [employee["name"] for employee in parsed_data])

    def test_import_employee_data_from_csv(self):
        csv_data = "4,Amy Brown,Analyst,Finance,2022-04-01,amy@example.com,4567890123,4.1\n"
        csv_data += "5,Mark Davis,Engineer,IT,2022-05-01,mark@example.com,9012345678,4.4\n"
        self.ems.import_employee_data_from_csv(csv_data)
        self.assertEqual(len(self.ems.employees), 5)
        self.assertIn(4, self.ems.employees)
        self.assertIn(5, self.ems.employees)

if __name__ == '__main__':
    unittest.main()