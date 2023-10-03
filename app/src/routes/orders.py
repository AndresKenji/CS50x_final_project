from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import order_actions, menu_actions
from ..db.database import get_db
from ..db.models import OrderDetailBase
from .. db.db_models import Menu, Meal, Food, Orders, Users
from . helpers import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/orders",
    tags=['orders']
)


@router.get('/')
def get_orders(request: Request,db: Session = Depends(get_db)):
    print("loading orders page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    menu, types, food= menu_actions.get_menu_details(db=db)
    customers = db.query(Users).filter(Users.rol_id == 4).all()
    body["customers"] = customers
    body["menu"] = menu
    body['orders'] = order_actions.get_order_details(db)
    return templates.TemplateResponse("orders.html", body)

@router.get('/get_order/{order_id}')
def get_order(order_id : int, db: Session = Depends(get_db)):
    return order_actions.get_order(db = db, order_id = order_id)

@router.post('/add_order')
async def add_order(request: Request,db: Session = Depends(get_db)):
    print("adding order")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id not in [1,2,3]:
         body['msg']="Not authorized for this operation"
         return templates.TemplateResponse("orders.html", body)
    
    formdata = await request.form()
    result_dict = {}
    details = []
    current_food_id = None
    current_quantity = None
    current_detail = None

    for key, value in formdata.items():
        if key.startswith('food_id'):
            current_food_id = value
        elif key.startswith('food_quantity'):
            current_quantity = int(value) if value.isdigit() else None
        elif key.startswith('detail'):
            current_detail = value if value else None

        if current_food_id and current_quantity is not None:
            result_dict[current_food_id] = {
                'quantity': current_quantity,
                'detail': current_detail
            }
    
    food_ids = result_dict.keys()

    for id in food_ids:
         detail = OrderDetailBase(
              food_id= id,
              food_quantity= result_dict[id]['quantity'],
              detail=result_dict[id]['detail'],
              user_id= formdata['customer_id']
         )
         details.append(detail)

    action = order_actions.add_order(db= db, details= details)

    if action:
        return RedirectResponse('/orders', status_code=status.HTTP_302_FOUND)
    else:
        body["msg"] = "There was an error, please verify the order"
        return templates.TemplateResponse("orders.html", body)

@router.post('/update_order/{order_id}')
async def update_order(request: Request,order_id: int, db: Session = Depends(get_db)):
    print(f"Updatting order {order_id}")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    formdata = await request.form()
    state_id = formdata['state_id']
    action = order_actions.update_order_state(order_id, state_id, db)
    if action:
         return RedirectResponse('/orders', status_code=status.HTTP_302_FOUND)
    body['msg'] = f'There was an error updating the order {order_id}'
    return templates.TemplateResponse("orders.html", body)

@router.get('/delete_order/{order_id}')
def delete_order(request: Request,order_id: int,db: Session = Depends(get_db)):
    print(f"Updatting order {order_id}")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    action = order_actions.delete_order(db=db,order_id=order_id)
    if action:
         return RedirectResponse('/orders', status_code=status.HTTP_302_FOUND)
    body['msg'] = f'There was an error updating the order {order_id}'
    return templates.TemplateResponse("orders.html", body)