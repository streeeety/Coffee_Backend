from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import pika
import json

from database import SessionLocal
from models import Order
from schemas import OrderCreate, OrderResponse
from auth import verify_token
from logger_config import get_logger

logger = get_logger()

router = APIRouter()

MENU_SERVICE_URL = "http://127.0.0.1:8002/drinks"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def send_order_to_queue(order_data):

    try:

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        channel = connection.channel()

        channel.queue_declare(
            queue="orders",
            durable=True
        )

        channel.basic_publish(
            exchange="",
            routing_key="orders",
            body=json.dumps(order_data),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        logger.info(f"Order sent to queue: {order_data}")

        connection.close()

    except Exception as e:

        logger.error(f"RabbitMQ error: {e}")


@router.post("/orders/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):

    try:

        logger.info("Creating order")

        response = requests.get(MENU_SERVICE_URL)

        if response.status_code != 200:

            raise HTTPException(
                status_code=503,
                detail="Menu service unavailable"
            )

        drinks = response.json()

        drink = None

        for d in drinks:
            if d["id"] == order.drink_id:
                drink = d
                break

        if drink is None:

            raise HTTPException(
                status_code=404,
                detail="Drink not found"
            )

        total_price = drink["price"] * order.quantity

        new_order = Order(
            customer_name=order.customer_name,
            drink_id=order.drink_id,
            quantity=order.quantity,
            total_price=total_price
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        send_order_to_queue({
            "order_id": new_order.id,
            "drink_id": new_order.drink_id,
            "quantity": new_order.quantity,
            "total_price": new_order.total_price
        })

        logger.info(f"Order created id={new_order.id}")

        return new_order

    except HTTPException:
        raise

    except Exception as e:

        logger.error(f"Unexpected error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/orders/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):

    try:

        orders = db.query(Order).all()

        return orders

    except Exception as e:

        logger.error(f"Error getting orders: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch orders"
        )