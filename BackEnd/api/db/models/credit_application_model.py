from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreditApplication(Base):
    __tablename__ = 'CreditApplication'

    credit_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer)
    address_id = Column(Integer)  # Assuming there is an Address table
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(String(100))
    marital_status = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    TIN = Column(String(20))