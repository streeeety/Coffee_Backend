from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Drink
from schemas import DrinkCreate, DrinkUpdate, DrinkOut

router = APIRouter()

# Подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET /drinks — все напитки
@router.get("/drinks", response_model=List[DrinkOut])
def get_drinks(db: Session = Depends(get_db)):
    return db.query(Drink).all()


# POST /drinks — создать напиток
@router.post("/drinks", response_model=DrinkOut)
def create_drink(drink: DrinkCreate, db: Session = Depends(get_db)):
    db_drink = Drink(**drink.dict())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink


# PUT /drinks/{id} — обновить напиток
@router.put("/drinks/{drink_id}", response_model=DrinkOut)
def update_drink(drink_id: int, drink: DrinkUpdate, db: Session = Depends(get_db)):
    db_drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    for key, value in drink.dict().items():
        setattr(db_drink, key, value)
    db.commit()
    db.refresh(db_drink)
    return db_drink


# DELETE /drinks/{id} — удалить напиток
@router.delete("/drinks/{drink_id}")
def delete_drink(drink_id: int, db: Session = Depends(get_db)):
    db_drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    db.delete(db_drink)
    db.commit()
    return {"message": "Drink deleted"}