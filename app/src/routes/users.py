import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from .. db import users_actions
from .. db.database import get_db
from .. db.models import UsersBase
from .. db.db_models import Users

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
def create_user(user:UsersBase,db: Session = Depends(get_db)):
    return users_actions.create_user(db=db,user=user)

@router.patch('/update_user')
def update_user(user:UsersBase,db: Session = Depends(get_db)):
    return users_actions.update_user(db=db, edit=user)

@router.delete('/delete_user/{id}')
def delete_user(id:int,db: Session = Depends(get_db)):
    return users_actions.delete_user(db=db, id=id)

@router.post('/change_roles/{id}')
def change_roles(id:int,rol_id:int,db: Session = Depends(get_db)):
    return users_actions.change_roles(db=db,id=id,rol_id=rol_id)

