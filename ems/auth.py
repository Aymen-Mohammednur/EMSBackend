from flask import Blueprint, request, jsonify, abort, make_response, session
from functools import wraps
from ems import app, db, bcrypt
from ems.models import User
import jwt
import datetime

bp = Blueprint('auth', __name__)

def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            currentUser = User.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if not currentUser.user_role != "manager":
            return {'message' : 'You are not authorized'}, 401

        return f(*args, **kwargs)

    return decorated

@bp.route('/login', methods=['POST'])
def login():
    # if current_user.is_authenticated():
    #     return jsonify({'message': "Already logged in"})

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return abort(404, "Could not verify")

    try:
        user = User.query.filter_by(username = auth.username).first()
        if not user:
            return abort(404, "Invalid credentials")
    
        if bcrypt.check_password_hash(user.password, auth.password):
            if user.user_role == "admin":
                token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
                # token = jwt.encode({'id' : user.id}, app.config['SECRET_KEY'], algorithm="HS256")
                # login_user(user)
                session["type"] = user.user_role
                # return jsonify({'message': "admin login successful"})
                response = jsonify({"username":user.username, "role":user.user_role,"token":token})
                return response
                
            elif user.user_role == "manager":
                token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
                # token = jwt.encode({'id' : user.id}, app.config['SECRET_KEY'], algorithm="HS256")
                # login_user(user)
                session["type"] = user.user_role
                # return jsonify({'message': "hr login successful"})
                response = jsonify({"username":user.username, "role":user.user_role,"token":token})
                return response
        else:
            return abort(404, "Invalid credentials")
            
    except Exception:
        return abort(404, "Invalid credentials")