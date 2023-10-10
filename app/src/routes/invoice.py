import json
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from .. db import invoice_actions, order_actions
from .. db.database import get_db
from .. db.models import InvoiceBase
from .. db.db_models import Invoice
from . helpers import get_current_user


templates = Jinja2Templates(directory="templates")
router = APIRouter()

router = APIRouter(
    prefix="/invoice",
    tags=['invoice']
)

@router.get('/get_invoice/{order_id}')
def get_invoice(order_id:int,db: Session = Depends(get_db)):
    return invoice_actions.create_invoice(db,order_id=order_id)

@router.get('/create_invoice/{order_id}')
def create_invoice(request:Request ,order_id:int, db:Session = Depends(get_db)):
    print("Inserting invoice to db")
    user, body = get_current_user(request=request, db=db)
    try:
        if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        if user.rol_id not in [1,3]:
            body["msg"] = "Unauthorized user getting back to home page"
            return templates.TemplateResponse("orders.html", body)
        
        invoice_detail = order_actions.get_order_detail(db, order_id)
        
        invoice = InvoiceBase(
            order_id=int(invoice_detail['id']),
            user_id=invoice_detail['user_id'],
            total=invoice_detail['total'],
            elementes= json.dumps(invoice_detail['details'])
        )

        print(invoice)

        invoice_db = invoice_actions.create_invoice(db, invoice) 
        if isinstance(invoice_db, Invoice):
            
            order_actions.update_order_state(order_id=order_id,state_id=4,db=db)
            return RedirectResponse('/orders', status_code=status.HTTP_302_FOUND)
        else:
            body['msg'] = "There is an error inserting the invoice on db, please contact an administrator"
            return templates.TemplateResponse('orders.html', body)
    except Exception as e:
        print(e)
    

