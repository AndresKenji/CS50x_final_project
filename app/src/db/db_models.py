from sqlalchemy import Column,Integer,String, ForeignKey, Date
from .database import Base, engine


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=True)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True, index=True)
    date = Column(Date, nullable=False)
    state_id = Column(Integer,ForeignKey('states.id'), nullable=False)
class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)

class States(Base):
    __tablename__ = "states"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)

class Food(Base):
    __tablename__ = "food"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    origin = Column(String)
    ingredients = Column(String, nullable=False)
    meal_id = Column(Integer,ForeignKey('meal.id'), nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)

class Drinks(Base):
    __tablename__ = 'drinks'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    origin = Column(String)
    ingredients = Column(String, nullable=False)
    meal_id = Column(Integer,ForeignKey('meal.id'), nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer,primary_key=True, index=True)
    food_id = Column(Integer,ForeignKey('food.id'), nullable=True)
    drink_id = Column(Integer,ForeignKey('drinks.id'), nullable=True)
    food_quantity = Column(Integer, nullable=True)
    drink_quantity = Column(Integer, nullable=True)


class OrderDetail(Base):
    __tablename__ = 'orderdetail'
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    food_id = Column(Integer,ForeignKey('food.id'), nullable=True)
    drink_id = Column(Integer,ForeignKey('drinks.id'), nullable=True)
    user_id = Column(Integer,ForeignKey('users.id'), nullable=False)
    detail = Column(String)
    food_quantity = Column(Integer, nullable=True)
    drink_quantity = Column(Integer, nullable=True)


class Invoice(Base):
    __tablename__ ='invoice'
    id = Column(Integer,primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    elementes = Column(String)
    total = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    date = Column(Date)


Base.metadata.create_all(bind=engine)