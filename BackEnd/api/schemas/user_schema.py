from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str
    birth_date: datetime

class UserUpdate(BaseModel):
    user_id: int = Field(..., gt=0, description="The user ID must be greater than zero")
    user_type_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class Register(BaseModel):
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str

class Login(BaseModel):
    email_phone: str
    password: str

