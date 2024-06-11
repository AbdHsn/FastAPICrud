from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PriceModel(Base):
    __tablename__ = 'PriceModel'  # Specify the name of the table if needed

    price_model_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Float)