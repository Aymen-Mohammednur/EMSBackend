from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import Attendance
from ems.schemas import attendance_schema, attendances_schema
from ems.auth import *

class AttendanceAPI(Resource):
    @token_required_manager
    def post(self):
        # try:
        #     attendance_schema.load(request.json)
        # except:
        #     abort(400, message="Invalid Request")

        if request.is_json:
            employee_id = request.json['employee_id']
            work_time = request.json["work_time"]
            date = request.json['date']
        else:
            employee_id = request.form['employee_id']
            work_time = request.form["work_time"]
            date = request.form['date']

        new_attendance = Attendance(work_time = work_time, employee_id=employee_id, date = date)
            
        db.session.add(new_attendance)
        db.session.commit()

        result = attendance_schema.dump(new_attendance)
        response = jsonify(result)
        response.status_code = 201
        return response
    @token_required_manager
    def get(self, attendance_id=None):
        if attendance_id:
            attendance = Attendance.query.filter_by(id=attendance_id).first()
            if attendance:
                result = attendance_schema.dump(attendance)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No attendnace record found")
        else:
            attendance = Attendance.query.all()
            if attendance:
                result = attendances_schema.dump(attendance)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No attendance records found")

    