from flask import Blueprint, request, jsonify, abort, make_response, session
from functools import wraps
from ems import app, db, bcrypt
from ems.models import User
import jwt
import datetime

bp = Blueprint('auth', __name__)

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
    
        
        else:
            return abort(404, "Invalid credentials")
            
    except Exception:
        return abort(404, "Invalid credentials")