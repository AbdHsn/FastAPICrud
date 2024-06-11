from sqlalchemy import Column, Integer, String
from db.base_class import Base

class UserType(Base):
    __tablename__ = 'UserType'

    user_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
