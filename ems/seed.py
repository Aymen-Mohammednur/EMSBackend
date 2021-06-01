 
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
@app.cli.command('db_random_employee')
@click.argument('arg')
def db_random_employee(arg):
    n = int(arg)
    # department_ids = [r.id for r in db.session.query(Department.c.id).distinct()]
    department_ids = [r.id for r in Department.query.all()]
    for i in range(n):
        d_o_b = get_random_date(1960, 2000).strftime("%d/%m/%Y")
        hourly = random.randint(7,25)
        employee = Employee(first_name = randomword(10), last_name = randomword(10), email = randomword(10), date_of_birth=d_o_b, hourly_rate=hourly, department_id=department_ids[random.randint(0,len(department_ids)-1)])
        db.session.add(employee)

    db.session.commit()
    print(f"{n} employees have been added.")


@app.cli.command('db_random_attendance')
@click.argument('arg')
def db_random_attendance(arg):
    n = int(arg)
    # department_ids = [r.id for r in db.session.query(Department.c.id).distinct()]
    employee_ids = [r.id for r in Employee.query.all()]
    for i in range(n):
        dateOfAttendance = get_random_date(1990, 2000).strftime("%d/%m/%Y")
        attendance = Attendance(work_time=random.randint(1,13), employee_id=employee_ids[random.randint(0,len(employee_ids)-1)], date=dateOfAttendance)
        db.session.add(attendance)

    db.session.commit()
    print(f"{n} attendance entries have been added.")


@app.cli.command('db_random_bonuscut')
@click.argument('arg')
def db_random_bonuscut(arg):
    n = int(arg)
    # department_ids = [r.id for r in db.session.query(Department.c.id).distinct()]
    employee_ids = [r.id for r in Employee.query.all()]
    for i in range(n):
        d_o_b = get_random_date(1960, 2000).strftime("%d/%m/%Y")
        bonus = BonusCuts(date = d_o_b, amount = (random.randint(5,50)*100), remark = randomword(20), employee_id=employee_ids[random.randint(0,len(employee_ids)-1)])
        db.session.add(bonus)

    db.session.commit()
    print(f"{n} bonuses/cuts have been added.")


@app.cli.command('db_show_all_department')
def db_show_departments():
    result = Department.query.all()
    for i in result: print(i)

@app.cli.command('db_show_all_employee')
def db_show_employee():
    result = Employee.query.all()
    for i in result: print(i)

@app.cli.command('db_show_all_attendance')
def db_show_attendance():
    result = Attendance.query.all()
    for i in result: print(i)
    
@app.cli.command('db_show_all_bonuscut')
def db_show_bonuscut():
    result = BonusCuts.query.all()
    for i in result: print(i)
