import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db import food_drink_actios
from ..db.database import get_db
from ..db.models import FoodBase, DrinksBase
from ..db.db_models import Food, Drinks

router = APIRouter(
    prefix="/food_drinks",
    tags=['food']
)

@router.post('/create_food')
def create_food(food: FoodBase,db: Session = Depends(get_db)):
    return food_drink_actios.create_food(db=db, food=food)

@router.post('/create_drink')
def create_drink(drink: DrinksBase,db: Session = Depends(get_db)):
    return food_drink_actios.create_drink(db=db, drink=drink)

@router.delete('/delete_food/{food_id}')
def delete_food(food_id:int,db: Session = Depends(get_db)):
    return food_drink_actios.delete_food(db=db, food_id=food_id)

@router.delete('/delete_drink/{drink_id}')
def delete_drink(drink_id:int,db: Session = Depends(get_db)):
    return food_drink_actios.delete_drink(db=db, drink_id=drink_id)

@router.patch('/update_food/{food_id}')
def update_food(food_id: int, food:FoodBase, db : Session = Depends(get_db)):
    return food_drink_actios.update_food(db=db, food_id=food_id, food=food)

@router.patch('/update_drink/{drink_id}')
def update_food(drink_id: int, drink:FoodBase, db : Session = Depends(get_db)):
    return food_drink_actios.update_drink(db=db, drink_id= drink_id, drink= drink)

@router.get('/get_food')
def get_food(db : Session = Depends(get_db)):
    return food_drink_actios.get_food(db=db)

@router.get('/get_drinks')
def get_drinks(db : Session = Depends(get_db)):
    return food_drink_actios.get_drinks(db=db)

@router.get('/get_one_food/{name}')
def get_one_food(name:str,db : Session = Depends(get_db)):
    return food_drink_actios.get_one_food(name=name, db=db)

@router.get('/get_drink/{name}')
def get_drink(name:str,db : Session = Depends(get_db)):
    return food_drink_actios.get_drink(name=name, db=db)