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
from .. db.db_models import Users, Roles
from . helpers import login_required, get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Loginform class for the login page
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')
    
# Home page resources
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
            USERNAME = user.name
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
    USERNAME = None
    
    return response

@router.get('/users',response_class=HTMLResponse)
def get_users_page(request: Request,response:Response, db: Session = Depends(get_db)):
    print("loading users page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id != 1:
        print("Unauthorized user getting back to home page")
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    users = db.query(Users.name, Users.last_name, Users.email, Roles.name.label('rol'))\
                .join(Roles, Roles.id == Users.rol_id)
    
    body["users"] = users
    
    return templates.TemplateResponse("users.html", body)

