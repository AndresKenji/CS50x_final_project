from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Local imports
from .. db import menu_actions
from .. db.database import get_db
from .. db.models import MenuBase
from .. db.db_models import Menu, Meal, Food
from . helpers import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/menu",
    tags=['menu']
)

@router.get('/', response_class=HTMLResponse)
def get_menu(request: Request,db: Session = Depends(get_db)):
    print("loading menu page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    menu, types, food= menu_actions.get_menu_details(db=db)
    meals = db.query(Meal).all()
    body["menu"] = menu
    body["types"] = types
    body["meals"] = meals
    body['food'] = food
    
    return templates.TemplateResponse("menu.html", body)

@router.post('/', response_class=HTMLResponse)
async def add_menu(request: Request,db: Session = Depends(get_db)):
    print("adding menu")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    try:
        formdata = await request.form()
        menu = MenuBase(
            food_id = formdata["food_id"] ,
            food_quantity = formdata["food_quantity"],
            type_id = (db.query(Food.type_id).filter(Food.id == formdata["food_id"]).first()).type_id
        )
        new_menu = menu_actions.add_menu(db=db, menu=menu)
        if isinstance(new_menu,Menu):
            return RedirectResponse(url="/menu",status_code=status.HTTP_302_FOUND)
        if isinstance(new_menu,str):
            body["msg"] = new_menu
            return templates.TemplateResponse("menu.html", body)
    except Exception as e:
        body["msg"] = e
        return templates.TemplateResponse("menu.html", body)
    

@router.get('/update_menu/{menu_id}', response_class=HTMLResponse)
async def update_menu(request: Request, menu_id: int, db: Session = Depends(get_db)):
    print("adding menu")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    try:
        formdata = await request.form()
        menu = MenuBase(
            food_id = None if formdata["food_id"] == None or formdata["food_id"] =="" else formdata["food_id"],
            drink_id = None if formdata["drink_id"] == None or formdata["drink_id"] =="" else formdata["drink_id"],
            food_quantity = None if formdata["food_quantity"] == None or formdata["food_quantity"] =="" else formdata["food_quantity"],
        )

        updated_menu = menu_actions.update_menu(db = db, menu_id = menu_id, menu = menu)
        if isinstance(updated_menu, Menu):
             return RedirectResponse(url="/menu",status_code=status.HTTP_302_FOUND)
        if isinstance(updated_menu, str):
            body["msg"] = updated_menu
            return templates.TemplateResponse("menu.html", body)
        
    except Exception as e:
            body["msg"] = e
            return templates.TemplateResponse("menu.html", body)

@router.get('/delete_menu/{menu_id}', response_class=HTMLResponse)
def delete_menu(request: Request,menu_id: int,db: Session = Depends(get_db)):
    print(f"Deleting menu {menu_id}")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    deleted_menu = menu_actions.delete_menu(db = db, menu_id = menu_id)
    return RedirectResponse(url="/menu",status_code=status.HTTP_302_FOUND)