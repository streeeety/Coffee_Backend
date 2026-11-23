# schemas.py
from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_name: str
    drink_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    drink_id: int
    quantity: int
    total_price: float

    class Config:
        orm_mode = True