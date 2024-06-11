from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import JSON

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = 'Vehicle'
    
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_model_id = Column(Integer)
    vehicle_type_id = Column(Integer)
    vehicle_color_id = Column(Integer) 
    price_model_id = Column(Integer)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    vin = Column(String(17), nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    status = Column(String(100), nullable=False)
    images = Column(JSON)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)