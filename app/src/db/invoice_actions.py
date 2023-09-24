from sqlalchemy.orm.session import Session
from .db_models import OrderDetail, Orders, Invoice,Food
import json
from datetime import datetime


def create_invoice(db:Session, order_id: int):
    _order = db.query(Orders).filter(Orders.id == order_id).first()
    _details = db.query(OrderDetail).all()

    if _order is None or _details is None:
        print(f'There is no order or detail with id {order_id}')

    _food = {name.id: name.name for name in db.query(Food.id, Food.name).all()}

    elements = []
    total = 0
    for element in _details:
        elements.append({_food[element.food_id] : element.food_quantity, "price": db.query(Food.price).filter(Food.id == element.food_id).first().price})
        
    try:
        new_invoice = Invoice()
        new_invoice.order_id = order_id
        new_invoice.elementes = json.dumps(elements)
        new_invoice.total = total
        new_invoice.user_id = _details[0].user_id
        new_invoice.date = datetime.now()

        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

        return new_invoice
    except Exception as e: 
        return str(e)







    