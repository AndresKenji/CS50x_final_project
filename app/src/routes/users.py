import json
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from . helpers import get_current_user

from .. db import users_actions
from .. db.database import get_db
from .. db.models import UsersBase
from .. db.db_models import Users, Roles

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get('/get_users')
def get_users(db: Session = Depends(get_db)):
    return users_actions.get_all_users(db=db)

@router.get('/get_user/{id}')
def get_user(id:int,db: Session = Depends(get_db)):
    return users_actions.get_user(db=db, id=id)

@router.post('/create_user')
async def create_user(request: Request,response:Response,db: Session = Depends(get_db)):
    try:
        print("Trying user creation")
        user, body = get_current_user(request=request, db=db)
        if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        if user.rol_id != 1:
            body["msg"] = "Unauthorized user getting back to home page"
            return templates.TemplateResponse("users.html", body)

        formdata = await request.form()
        user = UsersBase(
            name=formdata['name'],
            last_name= formdata['last_name'],
            email=formdata['email'],
            rol_id=formdata['rol'],
            password=formdata['password']
        )
        userdb = users_actions.create_user(db=db,user=user)
        if isinstance(userdb, Users):
            return RedirectResponse(url="/users/users",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        if isinstance(userdb, str):
            body["msg"] = userdb
            return templates.TemplateResponse("users.html", body)
    except Exception as e:
        body["msg"] = str(e)
        return templates.TemplateResponse("users.html", body)

@router.patch('/update_user')
def update_user(user:UsersBase,db: Session = Depends(get_db)):
    return users_actions.update_user(db=db, edit=user)

@router.delete('/delete_user/{id}')
def delete_user(id:int,db: Session = Depends(get_db)):
    return users_actions.delete_user(db=db, id=id)

@router.post('/change_roles/{id}')
def change_roles(id:int,rol_id:int,db: Session = Depends(get_db)):
    return users_actions.change_roles(db=db,id=id,rol_id=rol_id)



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