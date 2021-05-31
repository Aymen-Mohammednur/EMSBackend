from datetime import datetime
from flask import session
from ems import db
from safrs import SAFRSBase

class User( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.username}' ,'{self.user_role}')"