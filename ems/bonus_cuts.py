from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import BonusCuts
from ems.auth import db

class BonusCutsAPI(Resource):
    def post(self):
        if request.is_json:
            employee_id = request.json['employee_id']
            date = request.json['date']
            amount = request.json['amount']
            remark = request.json['remark']
        else:
            employee_id = request.form['employee_id']
            date = request.form['date']
            amount = request.form['amount']
            remark = request.form['remark']
        
        new_bonuscut = BonusCuts(employee_id=employee_id,date=date, amount=amount,remark=remark)
        
        db.session.add(new_bonuscut)
        db.session.commit()

    def get(self, bonus_id=None):
        if bonus_id:
            bonus = BonusCuts.query.filter_by(id=bonus_id).first()
            return bonus
        else:
            bonus = BonusCuts.query.all()
            return bonus

            
    