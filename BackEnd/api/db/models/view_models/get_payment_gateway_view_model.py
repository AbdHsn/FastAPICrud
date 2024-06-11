from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GetPaymentGatewaysView(Base):
    __tablename__ = 'GetPaymentGatewaysView'  # Specify the name of the view if needed

    gateway_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    implementation_details = Column(String(255))