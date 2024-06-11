from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GetWishesView(Base):
    __tablename__ = 'GetWishesView'  # Specify the name of the view if needed

    wish_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_type = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    vehicle_id = Column(Integer)
    vehicle_title = Column(String(255))
    created_at = Column(DateTime)
    status = Column(String(100))