from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Food, Drinks
from .models import FoodBase, DrinksBase

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

        db.add(new_food)
        db.commit()
        db.refresh(new_food)
        return new_food
    except Exception as e:
        return str(e)
    

def create_drink(db : Session, drink: DrinksBase) -> Drinks | str:
    _drinks = db.query(Drinks.name).all()
    if any(drink.name in tpl for tpl in _drinks):
        print('There is another drink with the same name')
        return 'There is another drink with the same name'
    
    try:
        new_drink = Drinks()
        new_drink.image_url = drink.image_url
        new_drink.name = drink.name
        new_drink.ingredients = drink.ingredients
        new_drink.origin = drink.origin
        new_drink.meal_id = drink.meal_id
        new_drink.price = drink.price

        db.add(new_drink)
        db.commit()
        db.refresh(new_drink)
        return new_drink
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

def delete_drink(db : Session, drink_id: int) -> bool:
    _drink = db.query(Drinks).filter(Drinks.id == drink_id).first()
    if  _drink == None:
        return False
    try:
        db.delete(_drink)
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

        db.add(_food)
        db.commit()
        db.refresh(_food)
        return _food
    except:
        return False

def update_drink(db : Session, drink_id: int, drink: DrinksBase) -> Drinks | bool:
    _drink = db.query(Drinks).filter(Drinks.id == drink_id).first()
    if  _drink == None:
        return False
    try:
        _drink.image_url = drink.image_url
        _drink.name = drink.name
        _drink.ingredients = drink.ingredients
        _drink.origin = drink.origin
        _drink.meal_id = drink.meal_id
        _drink.price = drink.price

        db.add(_drink)
        db.commit()
        db.refresh(_drink)
        return _drink
    except:
        return False

def get_food(db : Session) -> list[Food] | None:
    return db.query(Food).all()

def get_drinks(db: Session) -> list[Drinks] | None:
    return db.query(Drinks).all()

def get_one_food(name:str,db : Session) -> list[Food] | None:
    return db.query(Food).filter(Food.name == name).first()

def get_drink(name:str,db: Session) -> list[Drinks] | None:
    return db.query(Drinks).filter(Drinks.name == name).first()