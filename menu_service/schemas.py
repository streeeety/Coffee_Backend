from pydantic import BaseModel

class DrinkBase(BaseModel):
    name: str
    description: str
    price: float

class DrinkCreate(DrinkBase):
    pass

class DrinkUpdate(DrinkBase):
    pass

class DrinkOut(DrinkBase):
    id: int
    class Config:
        from_attributes = True