import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. db import menu_actions
from .. db.database import get_db
from .. db.models import MenuBase
from .. db.db_models import Menu

router = APIRouter(
    prefix="/menu",
    tags=['menu']
)

@router.get('/get_menu')
def get_menu(db: Session = Depends(get_db)):
    return menu_actions.get_menu(db=db)

@router.post('/add_menu')
def add_menu(menu: MenuBase,db: Session = Depends(get_db)):
    return menu_actions.add_menu(db=db, menu=menu)

@router.patch('/update_menu/{menu_id}')
def update_menu( menu_id: int, menu: MenuBase,db: Session = Depends(get_db)):
    return menu_actions.update_menu(db = db, menu_id = menu_id, menu = menu)

@router.delete('/delete_menu/{menu_id}')
def delete_menu(menu_id: int,db: Session = Depends(get_db)):
    return menu_actions.delete_menu(db = db, menu_id = menu_id)