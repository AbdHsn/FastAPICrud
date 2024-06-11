from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GetPriceModelsView(Base):
    __tablename__ = 'GetPriceModelsView'  # Specify the name of the view if needed

    price_model_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Float)

