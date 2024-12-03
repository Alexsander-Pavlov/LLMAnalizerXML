from pydantic import BaseModel
from datetime import date


class ProductSchema(BaseModel):
    """
    Схема продукта
    """
    uid: int
    id: int
    date: date
    name: str
    quantity: int
    price: float
    category: str
