from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.schemas import *
from ems.auth import *
from ems.attendance import *
from ems.bonus_cuts import *
from datetime import date
from sqlalchemy import func, select

def calculate_salary(employee_id):
    workHourSum = getWorkHourSum(employee_id)
    gross = workHourSum*getHourlyRate(employee_id)
    bonus = getBonusSum(employee_id)
    gross_with_bonus = gross + bonus
    net = gross_with_bonus - getTax()*gross_with_bonus
    return {"net":net, "gross":gross_with_bonus, "bonus":bonus}


def getTax():
    return .15


def getBonusSum(employee_id):
    bnc = db.session.query(func.sum(BonusCuts.amount)).filter_by(employee_id=employee_id).all()
    if not bnc[0][0]:
        return 0
    bon = BonusCuts.query.filter_by(employee_id=employee_id).all()
    for b in bon: db.session.delete(b)
    db.session.commit()
    return bnc[0][0]

    
def getWorkHourSum(employee_id):
    value = db.session.query(func.sum(Attendance.work_time)).filter_by(employee_id=employee_id).all()
    db.session.query(Attendance).filter_by(employee_id=employee_id).delete()
    db.session.commit()
    if not value[0][0]:
        return 0
    return value[0][0]

def getHourlyRate(employee_id):
    hourly_rate = Employee.query.filter_by(id=employee_id).first().hourly_rate
    return hourly_rate

class SalaryAPI(Resource):
    @token_required_manager
    def post(self):
        salary_date = None
        if request.is_json:
            if "date" in request.json: salary_date = request.json["date"]
            else: salary_date = datetime.datetime.now().strftime("%x")
            salary_amount = request.json['amount']
            salary_tax = request.json['tax']
            salary_net = request.json['total_amount']
            salary_employee_id = request.json['employee_id']
        else:
            if request.form["date"]: salary_date = request.form["date"]
            else: salary_date = datetime.datetime.now().strftime("%x")
            salary_amount = request.form['amount']
            salary_tax = request.form['tax']
            salary_net = request.form['net']
            salary_employee_id = request.form['employee_id']
        

        if salary_date:
            new_sal = Salary(date = salary_date, amount = salary_amount, tax = salary_tax, net = salary_net, employee_id = salary_employee_id)
        db.session.add(new_sal)
        db.session.commit()

        result = salary_schema.dump(new_sal)
        response = jsonify(result)
        response.status_code = 200
        return response

    @token_required_manager
    def get(self, emp_id):
        if not emp_id:
            abort(404, "unknown endpoint")

        print('hello, I\'m here')
        return_json = {}
        value = calculate_salary(emp_id)
        return_json["amount"] = value["gross"]
        return_json["tax"] = value["gross"]*getTax()
        return_json["bonus_cuts"] = value["bonus"]
        return_json["net"] = value["net"]
        return_json["date"] = str(date.today().month) + '/' + str(date.today().day) + '/' + str(date.today().year)
        response = jsonify(return_json)

        salary = Salary(date =return_json['date'],amount=return_json['amount'], tax=return_json['tax'], net=return_json['net'], employee_id=emp_id)
        db.session.add(salary)
        db.session.commit()

        response.status_code = 201
        return response

    @token_required_manager
    def delete(self, emp_id):
        sal = Salary.query.filter_by(employee_id=emp_id).first()
        if sal:
            db.session.delete(sal)
            db.session.commit()
            return jsonify(message="Salary successfully deleted"), 200
        else:
            abort(404, "No salary entry with that Id")
