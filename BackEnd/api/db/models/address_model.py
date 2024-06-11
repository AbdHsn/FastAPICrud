from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'Address'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)  # Assuming there is a User table
    address_type = Column(String(100))
    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))