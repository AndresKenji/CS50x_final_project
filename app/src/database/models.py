from pydantic import BaseModel
from typing import List, Optional

class UsersBase(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    rol_id: Optional[int]

class UsersCreate(UsersBase):
    pass

class Users(UsersBase):
    id: int

    class Config:
        orm_mode = True

class RolesBase(BaseModel):
    name: str

class RolesCreate(RolesBase):
    pass

class Roles(RolesBase):
    id: int

    class Config:
        orm_mode = True

class MealBase(BaseModel):
    name: str

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int

    class Config:
        orm_mode = True

class StatesBase(BaseModel):
    name: str

class StatesCreate(StatesBase):
    pass

class States(StatesBase):
    id: int

    class Config:
        orm_mode = True

class FoodBase(BaseModel):
    name: str
    origin: Optional[str]
    ingredients: str
    meal_id: int
    price: int
    image_url: Optional[str]

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int

    class Config:
        orm_mode = True

class DrinksBase(BaseModel):
    name: str
    origin: Optional[str]
    ingredients: str
    meal_id: int
    price: int
    image_url: Optional[str]

class DrinksCreate(DrinksBase):
    pass

class Drinks(DrinksBase):
    id: int

    class Config:
        orm_mode = True

class MenuBase(BaseModel):
    food_id: Optional[int]
    drink_id: Optional[int]
    food_quantity: Optional[int]
    drink_quantity: Optional[int]

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    food_id: Optional[int]
    drink_id: Optional[int]
    user_id: int
    state_id: Optional[int]
    detail: Optional[str]
    date: Optional[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    order_id: int
    elementes: str
    total: int
    user_id: int
    date: Optional[str]

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True