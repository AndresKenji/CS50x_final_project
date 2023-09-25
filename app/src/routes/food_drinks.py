from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# Local imports
from ..db import food_drink_actios
from ..db.database import get_db
from ..db.models import FoodBase
from ..db.db_models import Food
from . helpers import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/food",
    tags=['food']
)

@router.post('/create_food', response_class=HTMLResponse)
async def create_food(request: Request,db: Session = Depends(get_db)):
    print("adding food")
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    formdata = await request.form()
    food = FoodBase(
         name=formdata['name'],
         origin=formdata['origin'],
         type_id=formdata['type'],
         meal_id=formdata['meal'],
         ingredients=formdata['ingredients'],
         price=formdata['price'],
         image_url=formdata['image_url']
    )
    new_food = food_drink_actios.create_food(db=db, food=food)

    if isinstance(new_food, Food):
         return RedirectResponse(url="/menu",status_code=status.HTTP_302_FOUND)
    else:
         return RedirectResponse(url="/home",status_code=status.HTTP_306_RESERVED) 



@router.get('/delete_food/{food_id}')
def delete_food(request: Request,food_id:int,db: Session = Depends(get_db)):
    print("Deleting food")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    deleted_food = food_drink_actios.delete_food(db=db, food_id=food_id)
    return RedirectResponse(url='/menu',status_code=status.HTTP_302_FOUND)



@router.post('/update_food/{food_id}')
async def update_food(food_id: int, request: Request, db : Session = Depends(get_db)):
    user, body = get_current_user(request=request, db=db)
    if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    formdata = await request.form()
    food = FoodBase(
         name=formdata['name'],
         origin=formdata['origin'],
         type_id=formdata['type'],
         meal_id=formdata['meal'],
         ingredients=formdata['ingredients'],
         price=formdata['price'],
         image_url=formdata['image_url']
    )
    edited = food_drink_actios.update_food(db=db, food_id=food_id, food=food)
    return RedirectResponse(url='/menu',status_code=status.HTTP_302_FOUND)



@router.get('/get_food')
def get_food(db : Session = Depends(get_db)):
    return food_drink_actios.get_food(db=db)

@router.get('/get_one_food/{name}')
def get_one_food(name:str,db : Session = Depends(get_db)):
    return food_drink_actios.get_one_food(name=name, db=db)

