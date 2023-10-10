from sqlalchemy.orm.session import Session
from .db_models import OrderDetail, Orders, Invoice,Food
from .models import InvoiceBase
from datetime import datetime


def create_invoice(db:Session, invoice: InvoiceBase):

    try:
        invoice_db = Invoice()
        invoice_db.order_id = invoice.order_id
        invoice_db.date = datetime.now()
        invoice_db.total = invoice.total
        invoice_db.elementes = invoice.elementes
        invoice_db.user_id = invoice.user_id
        db.add(invoice_db)
        db.commit()
        db.refresh(invoice_db)

        return invoice_db
    except Exception as e:
        print(e)
        return None







    