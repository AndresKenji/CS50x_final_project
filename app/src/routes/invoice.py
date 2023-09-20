import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. db import invoice_actions
from .. db.database import get_db


router = APIRouter(
    prefix="/invoice",
    tags=['invoice']
)

@router.get('/get_invoice/{order_id}')
def get_invoice(order_id:int,db: Session = Depends(get_db)):
    return invoice_actions.create_invoice(db,order_id=order_id)

