import json
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from functools import wraps

from .. db import users_actions
from .. db.database import get_db
from .. db.models import UsersBase
from .. db.db_models import Users

templates = Jinja2Templates(directory="templates")
router = APIRouter()

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')

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
    try:
        user_id = request.cookies.get("user")
        print("Find user cookie = ",user_id)
        
        if user_id is None:
            print("User cookie not found")
            return None, {"request":request, "session":False, "rol":4}
        
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            print("User not found on db")
            return None, {"request":request, "session":False, "rol":4}
        print("User found on db")
        return user, {"request":request, "session":True, "rol":user.rol_id}
    except:
        return None, {"request":request, "session":False, "rol":4}
    

@router.get("/home", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    print("loading home page")
    user, body = get_current_user(request=request, db=db)
    print(body)
    return templates.TemplateResponse("home.html", body)

@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request, db:Session = Depends(get_db)):
    print("loading contact page")
    user, body = get_current_user(request=request, db=db)
    return templates.TemplateResponse("contact.html", body)


@router.get('/about', response_class=HTMLResponse)
def about(request:Request, db:Session = Depends(get_db)):
    print("loading about page")
    user, body = get_current_user(request=request, db=db)
    return templates.TemplateResponse("about.html",body)


@router.get("/login", response_class=HTMLResponse)
def login_get(request : Request, db:Session = Depends(get_db)):
    print("loading login page")
    user, body = get_current_user(request=request, db=db)
    return templates.TemplateResponse("login.html", body)

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request,
                     response: Response,
                     form_data: OAuth2PasswordRequestForm = Depends(),
                     db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        user = users_actions.authenticate_user(db=db,
                                            user=form_data.username,
                                            password=form_data.password)
        if user:
            response.set_cookie(key="user",value=user.id, httponly=True)
            return response
        else:
            return templates.TemplateResponse('login.html', {"request":request, "session":False, "msg":"Incorrect Username or Password", "rol":4})
    except Exception as e:
        print(e)
        return templates.TemplateResponse('login.html', {"request":request, "session":False, "msg":"Unkwon error", "rol":4})


@router.post("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = templates.TemplateResponse("home.html",{"request": request,"session":False, "rol":4})
    response.delete_cookie(key="user")
    
    return response