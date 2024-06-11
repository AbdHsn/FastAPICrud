from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Orders(Base):
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    vehicle_id = Column(Integer)
    price = Column(Float)
    status = Column(String(100))
    gateway_id = Column(Integer)
    payment_status = Column(String(100))
    start_date = Column(String(100))
    end_date = Column(String(100))  
    created_at = Column(String(100))
    updated_at = Column(String(100), nullable=True)