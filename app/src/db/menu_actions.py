from sqlalchemy.orm.session import Session
from .db_models import Menu, Food, Types
from .models import MenuBase

def add_menu(db: Session, menu: MenuBase) -> Menu | str:
    _menu = db.query(Menu.food_id).all()
    if any(menu.food_id in tpl for tpl in _menu):
        print('There is already a menu for this food')
        return 'There is already a menu for this food'
    try:
        if menu.food_id:
            new_menu = Menu()
            new_menu.food_id = menu.food_id
            new_menu.food_quantity = menu.food_quantity
            new_menu.type_id = menu.type_id
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

def update_menu(db: Session, menu_id: int, menu: MenuBase) -> Menu | None | str:
    _menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if _menu == None:
        return False
    
    try:
        if menu.food_id:
            _menu.food_id = menu.food_id
            _menu.food_quantity = menu.food_quantity
            _menu.type_id = menu.type_id
            db.add(_menu)
            db.commit()
            db.refresh(_menu)
            return _menu

    except Exception as e:
        return str(e)
    
    pass

def get_menu(db : Session) -> list[Menu] | None:
    return db.query(Menu).all()

def get_menu_details(db : Session):
    _food = db.query(Food).all()
    _menus = db.query(Menu).all()
    _types = db.query(Types).all()
    details = []


    for menu in _menus:
        detail = {}
        detail["id"] = menu.id
        detail["food_id"] = menu.food_id
        detail["amount"] = menu.food_quantity
        detail["type"] = next((tp.name for tp in _types if tp.id == menu.type_id), "Not found")
        detail["name"] = next((food.name for food in _food if food.id == menu.food_id), "Not found")
        detail["ingredients"] = next((food.ingredients for food in _food if food.id == menu.food_id),"Not found")
        detail["origin"] = next((food.origin for food in _food if food.id == menu.food_id),"Not found")
        detail["price"] = next((food.price for food in _food if food.id == menu.food_id),  "Not found")
        detail["image_url"] = next((food.image_url for food in _food if food.id == menu.food_id),  "Not found")
        details.append(detail)
    
    return details, _types, _food

