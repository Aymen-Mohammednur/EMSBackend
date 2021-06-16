from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import Department, db
from ems.auth import token_required_manager
from ems.schemas import departments_schema, department_schema

class DepartmentAPI(Resource):
    @token_required_manager
    def post(self):

        if request.is_json:
            title = request.json['department_title']
            no_of_employees = request.json['no_of_employees']
        else:
            title = request.form['department_title']
            no_of_employees = request.form['no_of_employees']

        dept = Department.query.filter_by(department_title=title).first()

        if dept:
            abort(409, message='Department already exists')
        else:
            new_dept = Department(department_title=title,
                                  no_of_employees=no_of_employees)
            
            db.session.add(new_dept)
            db.session.commit()

            result = department_schema.dump(new_dept)
            response = jsonify(result)
            response.status_code = 200
            return response

    @token_required_manager
    def get(self, dept_id=None):
        print("DEPARTMENT GET REQUEST RECIEVED")
        if dept_id:
            dept = Department.query.filter_by(id=dept_id).first()
            if dept:
                result = department_schema.dump(dept)
                response = jsonify(result)
                response.status_code = 201
                response.headers.add('Access-Control-Allow-Origin', '*')
                print("Response: ", response)
                return response

            else:
                abort(404, message="No department found")
        else:
            dept = Department.query.all()
            if dept:
                results = departments_schema.dump(dept)
                for i in range(len(dept)):
                    results[i]["department_title"] = dept[i].department_title
                    results[i]["no_of_employees"] = dept[i].no_of_employees
                response = jsonify(results)
                response.status_code = 201
                response.headers.add('Access-Control-Allow-Origin', '*')
                # print("datatype: ", type(result[1]))
                return response
            else:
                abort(404, message="No departments found")

    @token_required_manager
    def put(self, dept_id):
            
        dept = Department.query.filter_by(id=dept_id).first()
        if dept:
            if request.is_json:
                title = request.json['department_title']
                no_of_employees = request.json['no_of_employees']
            else:
                title = request.form['department_title']
                no_of_employees = request.form['no_of_employees']

            dept.department_title = title
            dept.no_of_employees = no_of_employees

            db.session.commit()

            result = department_schema.dump(dept)
            response = jsonify(result)
            response.status_code = 201
            return response

        else:
            abort(404, message="No department with that Id")

    @token_required_manager
    def delete(self, dept_id):
        dept = Department.query.filter_by(id=dept_id).first()
        if dept:
            db.session.delete(dept)
            db.session.commit()
            response = jsonify({"message":"Department successfully deleted"})
            response.status_code = 202
            return response
        else:
            abort(404, message="No department with that Id")