from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Wish(Base):
    __tablename__ = 'Wish'  # Specify the name of the table if needed

    wish_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    vehicle_id = Column(Integer)
    created_at = Column(DateTime)
    status = Column(String(100))