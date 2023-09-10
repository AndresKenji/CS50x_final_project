from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Food, Drinks
from .models import FoodBase, DrinksBase

def create_food(db: Session, food: FoodBase) -> Food | str:
    pass

def create_drink(db : Session, drink: DrinksBase) -> Drinks | str:
    pass

def delete_food(db: Session, food_id: int) -> bool:
    pass

def create_drink(db : Session, drink_id: int) -> bool:
    pass

def update_food(db: Session, food_id: int, food: FoodBase) -> Food | None:
    pass

def create_drink(db : Session, drink_id: int, drink: DrinksBase) -> Drinks | None:
    pass

def get_food(db : Session) -> list[Food] | None:
    pass

def get_drinks(db: Session) -> list[Drinks] | None:
    pass