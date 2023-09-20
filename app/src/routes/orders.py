import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db import order_actions
from ..db.database import get_db
from ..db.models import OrderDetailBase


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

@router.get('/get_orders')
def get_orders(db: Session = Depends(get_db)):
    return order_actions.get_orders(db = db)

@router.get('/get_order/{order_id}')
def get_order(order_id : int, db: Session = Depends(get_db)):
    return order_actions.get_order(db = db, order_id = order_id)

@router.post('/add_order')
def add_order(details: List[OrderDetailBase],db: Session = Depends(get_db)):
    return order_actions.add_order(db= db, details= details)

@router.patch('/update_order/{order_id}')
def update_order( order_id: int,detail: OrderDetailBase, detail_id: int, db: Session = Depends(get_db)):
    return order_actions.update_order(db=db, order_id=order_id, detail=detail, detail_id=detail_id)

@router.delete('/delete_order/{order_id}')
def delete_order(order_id: int,db: Session = Depends(get_db)):
    return order_actions.delete_order(db=db,order_id=order_id)