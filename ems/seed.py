 
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



@app.cli.command('db_seed')
def db_seed():
    admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    super_admin = User(username="admin", 
                       password=admin_password,
                       user_role="admin")

    manager_password = bcrypt.generate_password_hash('manager').decode('utf-8')
    manager = User(username="manager", 
                       password=manager_password,
                       user_role="manager")

    db.session.add(super_admin)
    db.session.add(manager)
    db.session.commit()
    print("Super admin and manager added")

@app.cli.command('db_random_department')
@click.argument('arg')
def db_random_department(arg):
    n = int(arg)
    for i in range(n):
        department = Department(department_title = randomword(7), no_of_employees = random.randint(50,100))
        db.session.add(department)
        db.session.commit()
    print(f"{n} departments have been added.")
