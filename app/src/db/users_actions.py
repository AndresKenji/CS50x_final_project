from sqlalchemy.orm.session import Session
from passlib.context import CryptContext

from .database import sessionLocal
from .db_models import Users, Roles
from .models import UsersBase


pwd_cxt = CryptContext(schemes='bcrypt')

class Hash():
    def bcrypt(password:str):
        return pwd_cxt.hash(password)
    def verify(hased_password, plain_password):
        return pwd_cxt.verify(plain_password, hased_password)


def create_user(db: Session, user: UsersBase) -> Users | str:
    users = db.query(Users.name, Users.email).all()
    _roles = db.query(Roles.id).all()
    
    if any(user.name in tpl for tpl in users):
        print("name already in use")
        return "name already in use"
    elif any(user.email in tpl for tpl in users):
        print("email already in use")
        return "email already in use"
    elif any(user.rol_id in tpl for tpl in _roles) == False:
        print("invalid rol")
        return "invalid rol"

    else:
        try:
            new_user = Users()
            new_user.name = user.name
            new_user.last_name = user.last_name
            new_user.email = user.email
            new_user.password = Hash.bcrypt(user.password)
            new_user.rol_id = user.rol_id if user.rol_id is not None else 4

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            return str(e)

        return new_user
    
def get_user(db: Session, id: int) -> Users | None:
    return db.query(Users).filter(Users.id == id).first()

def delete_user(db: Session, id:int) -> bool:
    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        return False
    
    db.delete(user)
    db.commit()
    
    return True

def update_user(db: Session, user : Users) -> Users | None:

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def get_all_users(db: Session) -> list[Users] | None:
    return db.query(Users).all()


def change_roles(db: Session, id : int, rol_id:int):
    _user = db.query(Users).filter(Users.id == id).first()
    _rol = db.query(Roles).filter(Roles.id == rol_id).first()
    if _user is None:
        print("User does not exists")
        return False
    if _rol is None:
        print("Role does not exist")
        return False
    
    try:
        _user.rol_id = rol_id
        db.add(_user)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    
def authenticate_user(db:Session, user: str, password: str) -> Users | bool:
    user = db.query(Users).filter(Users.name == user).first()
    if not user:
        return False
    if not Hash.verify(hased_password= user.password, plain_password=password):
        return False
    
    return user


