from sqlalchemy.orm.session import Session
from .database import sessionLocal
from .db_models import Menu
from .models import MenuBase

def add_menu(db: Session, menu: MenuBase) -> Menu | str:
    _menu = db.query(Menu.food_id).all()
    _drink = db.query(Menu.drink_id).all()
    if any(menu.food_id in tpl for tpl in _menu):
        print('There is already a menu for this food')
        return 'There is already a menu for this food'
    if any(menu.drink_id in tpl for tpl in _drink):
        print('There is already a menu for this drink')
        return 'There is already a menu for this drink'
    try:
        if menu.food_id:
            new_menu = Menu()
            new_menu.food_id = menu.food_id
            new_menu.food_quantity = menu.food_quantity
            db.add(new_menu)
            db.commit()
            db.refresh(new_menu)
            return new_menu
        if menu.drink_id:
            new_menu = Menu()
            new_menu.drink_id = menu.drink_id
            new_menu.drink_id = menu.drink_id
            db.add(new_menu)
            db.commit()
            db.refresh(new_menu)
            return new_menu
    except Exception as e:
        return str(e)

def delete_menu(db: Session, menu_id: int) -> bool:
    _menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if _menu == None:
        return False
    try:
        db.delete(_menu)
        db.commit()
        return True
    except:
        return False

def update_menu(db: Session, menu_id: int, menu: MenuBase) -> Menu | None:
    _menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if _menu == None:
        return False
    
    try:
        if menu.food_id:
            _menu.food_id = menu.food_id
            _menu.food_quantity = menu.food_quantity
            db.add(_menu)
            db.commit()
            db.refresh(_menu)
            return _menu
        if menu.drink_id:
            _menu.drink_id = menu.drink_id
            _menu.drink_id = menu.drink_id
            db.add(_menu)
            db.commit()
            db.refresh(_menu)
            return _menu
    except Exception as e:
        return str(e)
    
    pass

def get_menu(db : Session) -> list[Menu] | None:
    return db.query(Menu).all()

