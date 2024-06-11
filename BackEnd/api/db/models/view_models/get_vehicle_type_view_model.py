from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GetVehicleTypesView(Base):
    __tablename__ = 'GetVehicleTypesView'

    vehicle_type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
