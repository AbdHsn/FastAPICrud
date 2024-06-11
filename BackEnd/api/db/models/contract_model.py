from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contract(Base):
    __tablename__ = 'Contract'

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)  # Assuming there is a User table
    order_id = Column(Integer)  # Assuming there is an Orders table
    e_sign = Column(String)
    sign_date = Column(String)
    status = Column(String(100))
    policy_id = Column(Integer)
    policy = Column(String(255))