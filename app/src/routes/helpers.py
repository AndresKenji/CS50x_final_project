from fastapi import Request,status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from functools import wraps
from .. db.db_models import Users, Roles


def login_required(f):
    """
    Decorate routes to require login
    """
    @wraps(f)
    def decorated_function(*args, ** kwargs):
        if get_current_user() is None:
            response = RedirectResponse(url="/login", status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            return response
        return f(*args, ** kwargs)
    return decorated_function

def get_current_user(request: Request, db:Session):
    body = {"request":request, 
            "session":False, 
            "rol":4, 
            "msg":None,
            "USERNAME": None }
    try:
        user_id = request.cookies.get("user")
        print("Find user cookie = ",user_id)
        
        if user_id is None:
            print("User cookie not found")
            
            return None, body
        
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            print("User not found on db")
            return None, body
        print(f"User {user.name} found on db")
        body["rol"] = user.rol_id
        body["session"] = True
        body["USERNAME"] = user.name
        return user, body
    except:
        return None, body