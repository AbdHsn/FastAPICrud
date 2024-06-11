from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import json

Base = declarative_base()

class GetVehiclesView(Base):
    __tablename__ = 'GetVehiclesView'
    
    vehicle_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    vehicle_model_id = Column(Integer, ForeignKey('vehicle_models.vehicle_model_id'), nullable=False)
    vehicle_model = Column(String(255), nullable=False)
    vehicle_type_id = Column(Integer, ForeignKey('vehicle_types.vehicle_type_id'), nullable=False)
    vehicle_type = Column(String(100), nullable=False)
    vehicle_color_id = Column(Integer, ForeignKey('vehicle_colors.vehicle_color_id'))
    vehicle_color = Column(String(100))
    price_model_id = Column(Integer, ForeignKey('price_models.price_model_id'), nullable=False)
    price_model = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    vin = Column(String(17), nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    #images = Column(JSON)  # Using JSON type to store list of images
    images = Column(Text)
   # images = Column(JSON)
    status = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

