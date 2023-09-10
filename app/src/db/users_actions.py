from sqlalchemy.orm.session import Session
from passlib.context import CryptContext

from .database import sessionLocal
from .db_models import Users
from .models import UsersBase


pwd_cxt = CryptContext(schemes='bcrypt')

class Hash():
    def bcrypt(password:str):
        return pwd_cxt.hash(password)
    def verify(hased_password, plain_password):
        return pwd_cxt.verify(plain_password, hased_password)


def create_user(db: Session, user: UsersBase) -> Users | str:
    users = db.query(Users.name, Users.email).all()
    
    if any(user.name in tpl for tpl in users):
        print("name already in use")
        return "name already in use"
    elif any(user.email in tpl for tpl in users):
        print("email already in use")
        return "email already in use"
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
    
    

def delete_user(db: Session, email:str) -> bool:
    user = db.query(Users).filter(Users.email == email)
    if user is None:
        return False
    
    db.delete(user)
    db.commit()
    
    return True

def update_user(db: Session, edit : UsersBase) -> Users | None:

    user = db.query(Users).filter(Users.email == edit.email).first()
    if user is None:
        return "User does not exists"
    
    user.name = edit.name
    user.last_name = edit.last_name
    user.email = edit.email
    user.rol_id = edit.rol_id

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def get_all_users(db: Session) -> list[Users] | None:
    return db.query(Users.name, Users.email).all()

def get_user(db: Session, email: str) -> Users | None:
    return db.query(Users).filter(Users.email == email)

