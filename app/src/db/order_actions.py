from sqlalchemy.orm.session import Session
from datetime import datetime
from .db_models import OrderDetail, Orders, Food, Users
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
        for detail in details:
            order_detail = OrderDetail()
            order_detail.order_id = _new_order.id
            order_detail.food_id = detail.food_id
            order_detail.user_id = detail.user_id
            order_detail.food_quantity = detail.food_quantity if detail.food_quantity else None
            order_detail.detail = detail.detail if detail.detail else None
            
            order_details.append(order_detail)
        
        db.add_all(order_details)
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


def get_orders(db : Session) -> list[OrderDetailBase] | None:
    return db.query(OrderDetail).all()

def get_order(db:Session, order_id:int) -> list[OrderDetailBase] | None:
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()


def get_order_details(db:Session):
    _orders = db.query(Orders).all()
    _details = db.query(OrderDetail).all()
    _food = db.query(Food).all()
    _users = db.query(Users).all()
    details = []

    for order in _orders:
        detail = {}
        detail['id'] = order.id
        detail['user'] = next((user.name for user in _users if user.id == order.user_id), 'Not found')
        detail['details'] = next(())
        
        
        
        pass



    return details



