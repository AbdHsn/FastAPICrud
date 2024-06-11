from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GetOrdersView(Base):
    __tablename__ = 'GetOrdersView'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    user_type = Column(String(100))
    vehicle_id = Column(Integer)
    title = Column(String(255))
    price = Column(Integer)  # Adjust data type as per your requirement
    status = Column(String(100))
    gateway_id = Column(Integer)
    gateway = Column(String(255))
    credit_name = Column(String(100))
    credit_last_name = Column(String(100))
    credit_email = Column(String(255))
    credit_phone = Column(String(20))
    credit_tin = Column(String(20))
    contract_sign = Column(String(20))
    contract_status = Column(String(20))
    contract_sign_date = Column(DateTime)
    contract_policy = Column(String(255))
    payment_status = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
