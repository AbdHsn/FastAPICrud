from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'  # Specify the name of the table if needed

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_type_id = Column(Integer)
    email = Column(String(255))
    phone = Column(String(20))
    password = Column(String(255))  # Adjust length as per your requirements
    reset_token = Column(String(255))  # Adjust length as per your requirements
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(String(20), nullable=True)