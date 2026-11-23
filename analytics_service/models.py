from sqlalchemy import Column, Integer, Float
from database import Base


class Analytics(Base):

    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer)

    drink_id = Column(Integer)

    quantity = Column(Integer)

    total_price = Column(Float)