from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import Employee, Department, db
from ems.auth import token_required_manager
from ems.schemas import employee_schema, employees_schema
from collections import OrderedDict

class EmployeeAPI(Resource):
    @token_required_manager
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

    @token_required_manager
    def get(self, employee_id=None):
        if employee_id:
            employee = Employee.query.filter_by(id=employee_id).first()
            if employee:
                result = employee_schema.dump(employee)
                response = jsonify(result)
                response.status_code = 200
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                abort(404, message="No employee found")
        else:
            employee = Employee.query.all()
            
            if employee:
                results = employees_schema.dump(employee)
                cache = OrderedDict()
                print("RESULT:: ", results)
                for result in results:
                    dep_id = result["department_id"]
                    if not dep_id in cache:
                        dep = Department.query.filter_by(id=dep_id).first()
                        if dep:
                            cache[dep_id] = dep.department_title
                    if cache[dep_id]:
                        result["department_title"] = cache[dep_id]
                
                response = jsonify(results)
                response.status_code = 200
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                abort(404, message="No employees found")

    @token_required_manager
    def put(self, employee_id):
        # try:
        #     employee_schema.load(request.json)
        # except:
        #     abort(400, message="Invalid request")

        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
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
            
            employee.first_name=first_name
            employee.last_name=last_name
            employee.email=email
            employee.date_of_birth=date_of_birth
            employee.hourly_rate=hourly_rate
            employee.department_id=department_id

            db.session.commit()
            
            result = employee_schema.dump(employee)
            response = jsonify(result)
            response.status_code = 201
            return response
        
        else:
            abort(404, message="No employee with that Id")

    @token_required_manager
    def delete(self, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            response = jsonify({"message":"Employee successfully deleted"})
            response.status_code = 202
            return response
        else:
            abort(404, message="No employee with that Id")