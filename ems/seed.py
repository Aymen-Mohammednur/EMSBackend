 
import random
import datetime
from ems.models import BonusCuts, User, Department, Employee, Attendance, db
from ems import app, bcrypt
import string
import click

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_date(y1, y2):
    year = random.randint(y1, y2)
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')
    except ValueError:
        get_random_date(year)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("DB Created")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("DB Dropped")
