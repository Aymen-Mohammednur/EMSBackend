from flask import request, jsonify
from flask_restful import Resource, abort
from ems import bcrypt
from ems.models import User
from ems.schemas import user_schema, users_schema
from ems.auth import token_required_admin, db

class ManagerAPI(Resource):
    @token_required_admin
    def post(self):
        # try:
        #     user_schema.load(request.json)
        # except:
        #     abort(400, message="Invalid Request")

        if request.is_json:
            username = request.json['username']
            password = request.json['password']
            user_role = request.json['user_role']
        else:
            username = request.form['username']
            password = request.form['password']
            user_role = request.form['user_role']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_manager = User.query.filter_by(username=username).first()

        if new_manager:
            abort(409, message='User already exists')
        else:
            new_manager = User(username=username, password=hashed_password, user_role=user_role)
            
            db.session.add(new_manager)
            db.session.commit()

            result = user_schema.dump(new_manager)
            response = jsonify(result)
            response.status_code = 201
            return response
    
    @token_required_admin
    def get(self, user_id=None):
        if user_id:
            manager = User.query.filter_by(id=user_id).first()
            if manager:
                result = user_schema.dump(manager)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, message="No manager with that Id found")

        else:
            manager = User.query.all()
            if manager:
                result = users_schema.dump(manager)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, message="No users found")

    @token_required_admin
    def put(self, user_id):
        # try:
        #     user_schema.load(request.json)
        # except:
        #     abort(400, message="Invalid Request")
            
        manager = User.query.filter_by(id=user_id).first()
        if manager:
            if request.is_json:
                name = request.json['username']
                password = request.json['password']
                user_role = request.json['user_role']
            else:
                name = request.form['username']
                password = request.form['password']
                user_role = request.form['user_role']

            manager.username = name
            
            manager.user_role = user_role

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            manager.password = hashed_password
            
            db.session.commit()
            
            result = user_schema.dump(manager)
            response = jsonify(result)
            response.status_code = 200
            return response

        else:
            abort(404, message="No user with that Id")

    @token_required_admin
    def delete(self, user_id):
        manager = User.query.filter_by(id=user_id).first()
        if manager:
            db.session.delete(manager)
            db.session.commit()
            response = jsonify({"message":"Manager successfully deleted"})
            response.status_code = 202
            return response
        else:
            abort(404, message="No manager with that Id")