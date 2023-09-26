from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import order_actions
from ..db.database import get_db
from ..db.models import OrderDetailBase, OrdersBase
from .. db.db_models import Menu, Meal, Food, Orders
from . helpers import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/orders",
    tags=['orders']
)


@router.get('/')
def get_orders(request: Request,db: Session = Depends(get_db)):
    print("loading menu page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    body['orders'] = db.query(Orders).all()
    return templates.TemplateResponse("orders.html", body)

@router.get('/get_order/{order_id}')
def get_order(order_id : int, db: Session = Depends(get_db)):
    return order_actions.get_order(db = db, order_id = order_id)

@router.post('/add_order')
def add_order(details: OrderDetailBase,db: Session = Depends(get_db)):
    return order_actions.add_order(db= db, details= details)

@router.patch('/update_order/{order_id}')
def update_order( order_id: int,detail: OrderDetailBase, detail_id: int, db: Session = Depends(get_db)):
    return order_actions.update_order(db=db, order_id=order_id, detail=detail, detail_id=detail_id)

@router.delete('/delete_order/{order_id}')
def delete_order(order_id: int,db: Session = Depends(get_db)):
    return order_actions.delete_order(db=db,order_id=order_id)