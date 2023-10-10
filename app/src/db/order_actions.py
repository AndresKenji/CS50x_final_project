from sqlalchemy.orm.session import Session
from datetime import datetime
from .db_models import OrderDetail, Orders, Food, Users, States, Menu
from .models import OrderDetailBase
from typing import List


def add_order(db: Session, details: List[OrderDetailBase]) -> bool:
    # Create new order
    try:
        _new_order = Orders()
        _new_order.date = datetime.now()
        _new_order.state_id = 1
        db.add(_new_order)
        db.commit()
        db.refresh(_new_order)

        # add details
        order_details = []
        menu_subtraction = []
        for detail in details:
            _menu = db.query(Menu).filter(Menu.food_id == detail.food_id).first()
            if detail.food_quantity > _menu.food_quantity:
                db.delete(_new_order)
                db.commit()
                return False
            _menu.food_quantity = _menu.food_quantity - detail.food_quantity
            menu_subtraction.append(_menu)
            order_detail = OrderDetail()
            order_detail.order_id = _new_order.id
            order_detail.food_id = detail.food_id
            order_detail.user_id = detail.user_id
            order_detail.food_quantity = detail.food_quantity 
            order_detail.detail = detail.detail if detail.detail else None
            
            order_details.append(order_detail)
        
        db.add_all(order_details)
        db.add_all(menu_subtraction)
        db.commit()
        db.close()
    except:
        return False
    return True



def delete_order(db: Session, order_id: int) -> bool:
    _details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).first()
    _order = db.query(Orders).filter(Orders.id == order_id).first()
    if _details == None or _order == None:
        print("Order or detail not found")
        return False
    try:
        db.delete(_details)
        db.delete(_order)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_order(db: Session, order_id: int, detail: OrderDetailBase, detail_id: int) -> OrderDetailBase | bool:
    _detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).filter(OrderDetail.id == detail_id).first()
    _order = db.query(Orders).filter(Orders.id == order_id).first()
    if _detail == None or _order == None:
        print("Order or detail not found")
        return False
    else:
        _detail.order_id = _order.id
        _detail.food_id = detail.food_id
        _detail.food_quantity = detail.food_quantity if detail.food_quantity else None
        _detail.detail = detail.detail if detail.detail else None

        try:
            db.add(_detail)
            db.commit()
            db.refresh(_detail)
            return _detail
        except Exception as e:
            print(e)
            return False


def update_order_state(order_id: int, state_id:int,db : Session) :
    try:
        _order = db.query(Orders).filter(Orders.id == order_id).first()
        _order.state_id = state_id
        db.add(_order)
        db.commit()
    except:
        return False

    return True

def get_order(db:Session, order_id:int) -> list[OrderDetailBase] | None:
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()


def get_order_details(db:Session):
    _orders = db.query(Orders).all()
    _details = db.query(OrderDetail).all()
    _food = db.query(Food).all()
    _users = db.query(Users).all()
    _states = db.query(States).all()
    details = []

    for order in _orders:
        detail = {}
        detail['id'] = order.id
        detail['state_id'] = order.state_id
        detail['state'] = next((s.name for s in _states if s.id == order.state_id  ), 'None')
        detail['user_id'] = next((order_detail.user_id for order_detail in _details if order_detail.order_id == order.id), 'Not found')
        detail['user_name'] = next((user.name for user in _users if user.id == detail['user_id']), 'Not found')
        detail['details'] = {}
        detail['total'] = 0
        detail['order_details'] = [d for d in _details if d.order_id == order.id]
        for order_detail in detail['order_details']:
            detail['details'][order_detail.id] = {
            "food_id":order_detail.food_id,
            "food_name": next((f.name for f in _food if f.id == order_detail.food_id), "Not found"),
            "food_quantity":order_detail.food_quantity,
            "detail": order_detail.detail,
            "price": float(next((f.price for f in _food if f.id == order_detail.food_id), 0)) * int(order_detail.food_quantity)
            }
            detail['total'] += detail['details'][order_detail.id]['price']
            
        details.append(detail)  

    return details

def get_order_detail(db:Session, order_id:int):
    _order = db.query(Orders).filter(Orders.id == order_id).first()
    _details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
    _food = db.query(Food).all()
    _users = db.query(Users).all()
    _states = db.query(States).all()
    
    detail = {}
    detail['id'] = _order.id
    detail['state_id'] = _order.state_id
    detail['state'] = next((s.name for s in _states if s.id == _order.state_id  ), 'None')
    detail['user_id'] = next((order_detail.user_id for order_detail in _details if order_detail.order_id == _order.id), 'Not found')
    detail['user_name'] = next((user.name for user in _users if user.id == detail['user_id']), 'Not found')
    detail['details'] = {}
    detail['total'] = 0
    detail['order_details'] = [d for d in _details if d.order_id == _order.id]
    for order_detail in detail['order_details']:
        detail['details'][order_detail.id] = {
        "food_id":order_detail.food_id,
        "food_name": next((f.name for f in _food if f.id == order_detail.food_id), "Not found"),
        "food_quantity":order_detail.food_quantity,
        "detail": order_detail.detail,
        "price": float(next((f.price for f in _food if f.id == order_detail.food_id), 0)) * int(order_detail.food_quantity)
        }
        detail['total'] += detail['details'][order_detail.id]['price']
    
    return detail
    


