from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass


class Product(BaseModel):
    id: int
    name: str
    price: int
    description: str
    user_id: int


class Offer(BaseModel):
    name: str
    prod_id: int
    address: str
    offer_id: int
    user_id: int
