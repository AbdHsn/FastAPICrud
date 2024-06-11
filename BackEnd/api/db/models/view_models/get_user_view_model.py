from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class GetUsersView(Base):
    __tablename__ = 'GetUsersView'
    
    user_id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer)
    user_type = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(DateTime)

