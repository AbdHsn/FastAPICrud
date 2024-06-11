from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PaymentGateway(Base):
    __tablename__ = 'PaymentGateway'  # Specify the name of the table if needed

    gateway_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    implementation_details = Column(String(255))
