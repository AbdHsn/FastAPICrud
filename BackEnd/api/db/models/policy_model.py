from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Policy(Base):
    __tablename__ = 'Policy'  # Specify the name of the table if needed

    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    policy_type = Column(String(100))
    created_date = Column(DateTime)