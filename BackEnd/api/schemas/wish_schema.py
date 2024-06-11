from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WishCreate(BaseModel):
    user_id: int
    vehicle_id: int
    created_at: datetime
    status: str

class WishUpdate(BaseModel):
    wish_id: int = Field(..., gt=0, description="The wish ID must be greater than zero")
    user_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    created_at: Optional[datetime] = None
    status: Optional[str] = None
