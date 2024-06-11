from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.app_settings import settings
from typing import Generator

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator: #dependency injection
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()