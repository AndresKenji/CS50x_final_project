from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Roles
from .models import RolesBase



def create_rol(db: Session, rol: str) -> Roles | str:
    roles = db.query(Roles.name).all()
    if any(rol in tpl for tpl in roles):
        print("rol name already in use")
        return "rol name already in use"
    else:
        try:
            new_rol =Roles()
            new_rol.name = rol
            db.add(new_rol)
            db.commit()
            db.refresh(new_rol)
            return new_rol
        except Exception as e:
            return str(e)
    
    return 
    
    

def delete_rol(db: Session, rol:str) -> bool:
    role = db.query(Roles).filter(Roles.name == rol).first()
    if role is None:
        return False
    
    db.delete(role)
    db.commit()
    
    return True

def get_all_roles(db: Session) -> list[Roles] | None:
    return db.query(Roles).all()

