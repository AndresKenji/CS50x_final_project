from pydantic import BaseModel
from typing import List, Optional

class UsersBase(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    rol_id: Optional[int]

class TypesBase(BaseModel):
    name: str

class RolesBase(BaseModel):
    name: str

class MealBase(BaseModel):
    name: str

class StatesBase(BaseModel):
    name: str

class FoodBase(BaseModel):
    name: str
    origin: Optional[str]
    ingredients: str
    meal_id: int
    price: int
    image_url: Optional[str]
    type_id: int


class MenuBase(BaseModel):
    food_id: int
    food_quantity: int
    type_id: int

class OrdersBase(BaseModel):
    date: str

class OrderDetailBase(BaseModel):
    order_id: int
    food_id: Optional[int] = None
    user_id: int
    detail: Optional[str] = None
    food_quantity: Optional[int] = None

class InvoiceBase(BaseModel):
    order_id: int
    elementes: str
    total: int
    user_id: int
    date: Optional[str]
