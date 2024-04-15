from dataclasses import dataclass, asdict, field, replace
from datetime import datetime, date
from typing import Optional, List, Literal
import json

@dataclass
class Employee():
    employee_id: int
    name: str
    job_title: str
    department_id: int
    start_date: date
    email: str
    phone_number: str
    hourly_rate: float
    performance_rating: Optional[float] = None

@dataclass
class EmployeeTransfer():
    transfer_id: int
    employee_id: int
    previous_department_id: int
    new_department_id: int

@dataclass
class TimeSheet():
    timesheet_id: int
    employee_id: int
    date: date
    hours_worked: float

@dataclass
class Payroll():
    payroll_id: int
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    total_hours: float
    gross_pay: float
    taxes: float
    net_pay: float

@dataclass
class Department():
    department_id: int
    name: str


def get_new_id(table: dict) -> int:
    if len(table)==0:
        return 0
    else:
        return max(list(table.keys()))+1

class EmployeeManager():
    def __init__(self):
        self.employees = {}
        self.transfers = {}
    
    def create_employee(self, employee_id: int, name: str, job_title: str, 
                        department_id: int, start_date: date, email: str, 
                        phone_number: str, hourly_rate: float, performance_rating=None) -> None:
        if employee_id in self.employees.keys():
            raise Exception
        
        self.employees[employee_id] = Employee(employee_id, name, job_title, department_id, start_date, email, phone_number, hourly_rate, performance_rating)

    def get_employee(self, employee_id: int) -> Employee:
        
        if employee_id not in self.employees.keys():
            raise Exception
        
        return self.employees[employee_id]
    
    def get_employees_by_job_title(self, job_title: str) -> List[Employee]:
        return [e for e in self.employees.values() if e.job_title==job_title]
    
    def get_employees_by_department(self, department_id: int) -> List[Employee]:
        return [e for e in self.employees.values() if e.department_id==department_id]
    
    def calculate_average_performance_rating(self, department: str) -> Optional[float]:
        ratings = [
            e.performance_rating 
            for e in self.employees.values() 
            if e.department==department
            and e.performance_rating != None
        ]

        if len(ratings)==0:
            return None
        else:
            return sum(ratings) / len(ratings)
        
    def get_top_performers(self, n: int, department_id: Optional[int]=None) -> List[Employee]:
        
        if department_id:
            employee_list = self.get_employees_by_department(department_id)
        else:
            employee_list = [e for e in self.employees.values()]
        
        sorted_employees = sorted(
            employee_list,
            key=lambda x: (-x.performance_rating)
        )

        end_index = n
        while len(sorted_employees) >= end_index and sorted_employees[end_index].performance_rating == sorted_employees[end_index - 1].performance_rating:
            end_index += 1

        return sorted_employees[:min(end_index, len(sorted_employees))]
    
    def filter_employees_by_start_date(self, start_date: date) -> List[Employee]:
        return [e for e in self.employees.values() if e.start_date >= start_date]
    
    def export_employee_data_to_json(self) -> str:
        return json.dumps([asdict(e) for e in self.employees.values()], default=str)
    
    def import_employee_data_from_csv(self, csv_data: str) -> None:
        for s in csv_data.splitlines():
            args = s.split(',')
            id = int(args[0])
            name = args[1]
            job_title = args[2]
            department_id = int(args[3])
            start_date = datetime.strptime(args[4], '%Y-%m-%d')
            email = args[5]
            phone_number = args[6]
            hourly_rate = float(args[7])
            performance_rating = float(args[8])
            self.employees[id] = Employee(id, name, job_title, department_id, start_date, email, phone_number, hourly_rate, performance_rating)

    def update_employee_details(self, employee_id: int, **kwargs):
        self.employees[employee_id] = replace(self.employees[employee_id], **kwargs)

    def promote_employee(self, employee_id: int, new_job_title: str, salary_increment: float) -> None:
        self.update_employee_details(employee_id, job_title=new_job_title, hourly_rate=self.employees[employee_id].hourly_rate+salary_increment)

    def transfer_employee(self, employee_id: int, new_department_id: int) -> None:
        original_dept = self.employees[employee_id].department_id
        self.update_employee_details(employee_id, department_id=new_department_id)
        transfer_id = get_new_id(self.transfers)
        self.transfers[transfer_id] = EmployeeTransfer(transfer_id, employee_id, original_dept, new_department_id)

    def get_employee_transfer_history(self, employee_id: int) -> List[EmployeeTransfer]:
        return [t for t in self.transfers.values() if t.employee_id==employee_id]


class TimeSheetManager():
    def __init__(self):
        self.timesheets = {}

    def record_timesheet(self, timesheet_id: int, employee_id: int, date: date, hours_worked: float) -> None:
        # if employee_id not in self.employees.keys():
        #     raise Exception
        if timesheet_id in self.timesheets.keys():
            raise Exception
        
        self.timesheets[timesheet_id] = TimeSheet(timesheet_id, employee_id, date, hours_worked)

    def get_timesheet(self, timesheet_id: int) -> TimeSheet:
        if timesheet_id not in self.timesheets.keys():
            raise Exception
        
        return self.timesheets[timesheet_id]


class EmployeeManagementSystem():
    def __init__(self):
        self.employee_manager = EmployeeManager()
        self.timesheet_manager = TimeSheetManager()
        self.payrolls = {}
        self.departments = {}

    def create_employee(self, employee_id: int, name: str, job_title: str, 
                        department_id: int, start_date: date, email: str, 
                        phone_number: str, hourly_rate: float, performance_rating=None) -> None:
        self.employee_manager.create_employee(employee_id, name, job_title, department_id, start_date, email, phone_number, hourly_rate, performance_rating)
        
    def record_timesheet(self, timesheet_id: int, employee_id: int, date: date, hours_worked: float) -> None:
        self.timesheet_manager.record_timesheet(timesheet_id, employee_id, date, hours_worked)

    def get_employee(self, employee_id: int) -> Employee:
        return self.employee_manager.get_employee(employee_id)
    
    def get_timesheet(self, timesheet_id: int) -> TimeSheet:
        return self.timesheet_manager.get_timesheet(timesheet_id)
    
    def calculate_total_hours(self, employee_id: int, start_date: date, end_date: date) -> float:
        if employee_id not in self.employee_manager.employees.keys():
            raise Exception
        
        running_total = 0
        for t in self.timesheet_manager.timesheets.values():
            if t.employee_id==employee_id and t.date >= start_date and t.date < end_date:
                running_total += t.hours_worked

        return running_total
    
    def get_employees_by_job_title(self, job_title: str) -> List[Employee]:
        return self.employee_manager.get_employees_by_job_title(job_title)
    
    def get_employees_by_department(self, department_id: int) -> List[Employee]:
        return self.employee_manager.get_employees_by_department(department_id)

    def calculate_average_performance_rating(self, department: str) -> Optional[float]:
        return self.employee_manager.calculate_average_performance_rating(department)
        
    def get_top_performers(self, n: int) -> List[Employee]:
        return self.employee_manager.get_top_performers(n)
    
    def filter_employees_by_start_date(self, start_date: date) -> List[Employee]:
        return self.employee_manager.filter_employees_by_start_date(start_date)
    
    def export_employee_data_to_json(self) -> str:
        return self.employee_manager.export_employee_data_to_json()
    
    def import_employee_data_from_csv(self, csv_data: str) -> None:
        self.employee_manager.import_employee_data_from_csv(csv_data)

    def create_payroll(self, payroll_id: int, employee_id: int, pay_period_start: date, pay_period_end: date) -> None:
        
        total_hours = self.calculate_total_hours(employee_id, pay_period_start, pay_period_end)
        employee = self.employee_manager.employees[employee_id]
        gross_pay = employee.hourly_rate * total_hours
        tax_rate = 0.20
        taxes = gross_pay * tax_rate
        net_pay = gross_pay - taxes 
        
        self.payrolls[payroll_id] = Payroll(payroll_id, employee_id, pay_period_start, pay_period_end, 
                                            total_hours, gross_pay, taxes, net_pay)
        
    def get_payroll_by_id(self, payroll_id: int) -> Payroll:
        return self.payrolls[payroll_id]
    
    def get_employee_payrolls(self, employee_id: int) -> List[Payroll]:
        return [p for p in self.payrolls.values() if p.employee_id==employee_id]
    
    def update_employee_details(self, employee_id: int, **kwargs) -> None:
        self.employee_manager.update_employee_details(employee_id=employee_id, **kwargs)

    def calculate_employee_salary(self, employee_id: int, start_date: date, end_date: date) -> float:
        running_total = 0

        for p in self.payrolls.values():
            print(p)
            if p.employee_id == employee_id and p.pay_period_start >= start_date and p.pay_period_end < end_date:
                running_total += p.net_pay

        return running_total
    
    def promote_employee(self, employee_id: int, new_job_title: str, salary_increment: float) -> None:
        self.employee_manager.promote_employee(employee_id, new_job_title, salary_increment)

    def create_department(self, department_id: int, name: str) -> None:
        self.departments[department_id] = Department(department_id, name)

    def get_department(self, department_id: int) -> Department:
        return self.departments[department_id]
    
    def transfer_employee(self, employee_id: int, new_department_id: int) -> None:
        self.employee_manager.transfer_employee(employee_id, new_department_id)

    def get_employee_transfer_history(self, employee_id: int) -> List[EmployeeTransfer]:
        return self.employee_manager.get_employee_transfer_history(employee_id)
    
    def calculate_department_salary_expenditure(self, department_id: int, start_date: date, end_date: date) -> float:
        employees = [e.employee_id for e in self.get_employees_by_department(department_id)]
        running_total = 0.0

        for e in employees:
            running_total += self.calculate_employee_salary(e, start_date, end_date)

        return running_total
    
    def get_top_performing_employees(self, department_id: int, top_n: int) -> List[Employee]:
        return self.employee_manager.get_top_performers(top_n, department_id=department_id)
    