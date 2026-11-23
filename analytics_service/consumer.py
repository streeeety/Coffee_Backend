import pika
import json

from database import SessionLocal
from models import Analytics


def callback(ch, method, properties, body):

    data = json.loads(body)

    db = SessionLocal()

    order = Analytics(
        order_id=data["order_id"],
        drink_id=data["drink_id"],
        quantity=data["quantity"],
        total_price=data["total_price"]
    )

    db.add(order)
    db.commit()
    db.close()

    print("Order saved to analytics")


def start_consumer():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()

    # очередь должна быть объявлена одинаково
    channel.queue_declare(queue="orders", durable=True)

    channel.basic_consume(
        queue="orders",
        on_message_callback=callback,
        auto_ack=True
    )

    print("Waiting for orders...")

    channel.start_consuming()