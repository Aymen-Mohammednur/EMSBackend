from ems import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'username', 'password', 'user_role')
    username = fields.String(required=True)
    password = fields.String(required=True)
    user_role = fields.String(required=True)

class EmployeeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'hourly_rate', 'department_id')
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    date_of_birth = fields.String(required=True)
    hourly_rate = fields.Float(required=True)
    department_id = fields.Integer(required=True)
class DepartmentSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'department_title', 'no_of_employees')
    no_of_employees = fields.Integer(required=True)
    department_title = fields.String(required=True)
    


class AttendanceSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'work_time', 'employee_id', 'date')
    work_time = fields.Float(required=True)
    employee_id = fields.Integer(required=True)
    date = fields.String(required=True)

class BonusSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'date', 'amount', 'remark', 'employee_id')
    date = fields.String(required=True)
    amount = fields.Float(required=True)
    remark = fields.String(required=True)
    employee_id = fields.Integer(required=True)

class SalarySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'date', 'amount', 'tax', 'net', 'employee_id')
    date = fields.String(required=True)
    amount = fields.Float(required=True)
    tax = fields.Float(required=True)
    net = fields.String(required=True)
    employee_id = fields.Integer(required=True)