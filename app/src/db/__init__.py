from sqlalchemy import sql
from .users_actions import create_user
from .roles_actions import create_rol
from .db_models import Users, Roles, States, Meal, Types
from .models import UsersBase
from .database import sessionLocal
import time

def time_wait(times:int=1):
    for i in range(times):
        print("...")
        time.sleep(0.5)

db = sessionLocal()

if len(db.query(Roles).all()) == 0:
    print("Starting database for the first time, creating Roles")
    time_wait()
    create_rol(db=db, rol='administrator')
    time_wait()
    create_rol(db=db, rol='chef')
    time_wait()
    create_rol(db=db, rol='waiter')
    time_wait()
    create_rol(db=db, rol='customer')

if len(db.query(Users).all()) == 0:

    print("Creating user administrator")
    time_wait()
    new_user = UsersBase(name="admin",
                        last_name="administrator",
                        email="admin@local.com",
                        password="4dm1n1str4t0r",
                        rol_id=1)

    create_user(db=db,user=new_user)

if len(db.query(States).all()) == 0:
    print("Creating food states")

    db.execute(sql.text("INSERT INTO states (name) VALUES ('ordered'), ('cooking'),('serve'),('finished'),('canceled');"))
    time_wait(2)

if len(db.query(Meal).all()) == 0:
    print("Creating meal types")
    db.execute(sql.text("INSERT INTO meal (name) VALUES ('breakfast'), ('lunch'),('dinner'),('brunch'),('casual');"))
    time_wait(2)

if len(db.query(Types).all()) == 0:
    print("Creating food types")
    db.execute(sql.text("INSERT INTO types (name) VALUES ('food'), ('drink'),('dessert'),('special');"))
    time_wait(2)    

db.commit()
db.close()
    


