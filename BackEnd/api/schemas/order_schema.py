from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class OrderCreate(BaseModel):
    #order_id: int
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    vehicle_id: int
    title: str
    price: Optional[float]
    gateway_id: Optional[int]
    gateway: Optional[str]
    credit_name: Optional[str]
    credit_last_name: Optional[str]
    credit_email: Optional[str]
    credit_phone: Optional[str]
    credit_birth_date: Optional[datetime]
    credit_tin: Optional[str]
    credit_marital_status: Optional[str]
    contract_sign: Optional[str]
    contract_status: Optional[str]
    contract_sign_date: Optional[datetime]
    contract_policy: Optional[str]
    payment_status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    city: str                
    state: str         
    postal_code: str
    street: Optional[str] 
    # created_at: datetime
    # updated_at: Optional[datetime]