from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import Employee, Department, db
from ems.auth import token_required_manager
from ems.schemas import employee_schema, employees_schema
from collections import OrderedDict

class EmployeeAPI(Resource):
    def post(self):
        print("**********")
        print("Response: ", request)
        print("**********")
            
        if request.is_json:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            email = request.json['email']
            date_of_birth = request.json['date_of_birth']
            hourly_rate = request.json['hourly_rate']
            department_id = request.json['department_id']
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            date_of_birth = request.form['date_of_birth']
            hourly_rate = request.form['hourly_rate']
            department_id = request.form['department_id']

        employee = Employee.query.filter_by(email=email).first()

        if employee:
            abort(409, message="Employee with that email address already exists")
        else:
            new_employee = Employee(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    date_of_birth=date_of_birth,
                                    hourly_rate=hourly_rate,
                                    department_id=department_id)
            
            db.session.add(new_employee)
            db.session.commit()

            result = employee_schema.dump(new_employee)
            response = jsonify(result)
            response.status_code = 201
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response