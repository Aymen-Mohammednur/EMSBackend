from datetime import datetime
from flask import session
from ems import db
from safrs import SAFRSBase

class User( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.username}' ,'{self.user_role}')"

class Employee( db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    #date_of_birth = db.Column(db.DateTime, nullable=True, default=datetime.now)
    date_of_birth = db.Column(db.String, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    attendance = db.relationship('Attendance', backref='attend', lazy=True)
    bonus = db.relationship('BonusCuts', backref='bonus', lazy=True)
    salary = db.relationship('Salary', backref='salary', lazy=True)

    def __repr__(self):
        return f"Employee('ID: {self.id}\n{self.first_name}', '{self.last_name}', '{self.email}' ,'{self.department_id}')\n\n"

class Department( db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    department_title = db.Column(db.String, nullable=False)
    no_of_employees = db.Column(db.Integer, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True, cascade="all,delete")

    def __repr__(self):
        return f"Department('{self.department_title}', '{self.no_of_employees}')"
class Attendance( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    work_time = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f"Attendance('Emplyee ID: {self.employee_id}',Date: {self.date}, Hours Worked: '{self.work_time}')"

class BonusCuts( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"BonusCuts('{self.date}', '{self.amount}', '{self.employee_id}')"
class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Salary('{self.date}', '{self.amount}', '{self.net}', '{self.employee_id}')"