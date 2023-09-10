from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Food, Drinks, Menu
from .models import FoodBase, DrinksBase, MenuBase

def add_menu(db: Session, menu: MenuBase) -> Menu | str:
    pass

def delete_menu(db: Session, menu_id: int) -> bool:
    pass

def update_menu(db: Session, menu_id: int, menu: MenuBase) -> Food | None:
    pass

def get_menu(db : Session) -> list[Menu] | None:
    pass

