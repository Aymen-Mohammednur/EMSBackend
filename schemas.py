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