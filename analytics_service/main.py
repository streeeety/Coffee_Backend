from fastapi import FastAPI
import threading

from consumer import start_consumer
from database import Base, engine, SessionLocal
from models import Analytics

app = FastAPI(title="Analytics Service")

# создаём таблицы
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup():

    thread = threading.Thread(target=start_consumer)
    thread.daemon = True
    thread.start()


@app.get("/")
def root():
    return {"message": "Analytics service running"}


@app.get("/analytics")
def get_analytics():

    db = SessionLocal()

    orders = db.query(Analytics).all()

    total_orders = len(orders)
    total_revenue = sum(order.total_price for order in orders)

    db.close()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }