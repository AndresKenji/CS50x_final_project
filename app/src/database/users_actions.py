from sqlalchemy.orm.session import Session
from passlib.context import CryptContext

import database as db
import db_models as dbm
import models



pwd_cxt = CryptContext(schemes='bcrypt')

class Hash():
    def bcrypt(password:str):
        return pwd_cxt.hash(password)
    def verify(hased_password, plain_password):
        return pwd_cxt.verify(plain_password, hased_password)


def create_user(db: Session):
    pass

def delete_user(db: Session):
    pass

def update_user(db: Session):
    pass

def get_all_users(db: Session):
    pass

def get_user(db: Session):
    pass

