from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Food
from .models import FoodBase

def create_food(db: Session, food: FoodBase) -> Food | str:
    _food = db.query(Food.name).all()
    if any(food.name in tpl for tpl in _food):
        print('There is another food with the same name')
        return 'There is another food with the same name'
    
    try:
        new_food = Food()
        new_food.image_url = food.image_url
        new_food.name = food.name
        new_food.ingredients = food.ingredients
        new_food.origin = food.origin
        new_food.meal_id = food.meal_id
        new_food.price = food.price
        new_food.type_id = food.type_id

        db.add(new_food)
        db.commit()
        db.refresh(new_food)
        return new_food
    except Exception as e:
        return str(e)
    

def delete_food(db: Session, food_id: int) -> bool:
    _food = db.query(Food).filter(Food.id == food_id).first()
    if  _food == None:
        return False
    try:
        db.delete(_food)
        db.commit()
        return True
    except:
        return False

def update_food(db: Session, food_id: int, food: FoodBase) -> Food | bool:
    _food = db.query(Food).filter(Food.id == food_id).first()
    if  _food == None:
        return False
    try:
        _food.image_url = food.image_url
        _food.name = food.name
        _food.ingredients = food.ingredients
        _food.origin = food.origin
        _food.meal_id = food.meal_id
        _food.price = food.price
        _food.type_id = food.type_id

        db.add(_food)
        db.commit()
        db.refresh(_food)
        return _food
    except:
        return False

def get_food(db : Session) -> list[Food] | None:
    return db.query(Food).all()

def get_one_food(id:int,db : Session) -> Food | None:
    return db.query(Food).filter(Food.id == id).first()

    return db.query(Drinks).filter(Drinks.name == name).first()