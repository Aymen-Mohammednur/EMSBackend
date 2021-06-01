from flask import Flask, json
from flask.helpers import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import logging
from safrs import SAFRSAPI

app = Flask(__name__)
CORS(app)

logging.getLogger('flask_cors').level = logging.DEBUG

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SECRET_KEY'] = 'oursupersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
api = Api(app)
ma = Marshmallow(app)

from ems.seed import *
from ems.errors.handlers import errors

from ems.models import *

from ems import employee, department, attendance, auth, bonus_cuts, manager, salary


app.register_blueprint(auth.bp)
app.register_blueprint(errors)

api.add_resource(employee.EmployeeAPI, '/employees', '/employees/<int:employee_id>')

api.add_resource(department.DepartmentAPI, '/departments', '/departments/<int:dept_id>')

api.add_resource(manager.ManagerAPI, '/managers', '/managers/<int:user_id>')

api.add_resource(bonus_cuts.BonusCutsAPI, '/bonus')

api.add_resource(salary.SalaryAPI, '/salary/<int:emp_id>')

api.add_resource(attendance.AttendanceAPI, '/attendance')
