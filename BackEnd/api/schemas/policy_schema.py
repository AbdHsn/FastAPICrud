from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PolicyCreate(BaseModel):
    description: str
    policy_type: str
    created_date: datetime

class PolicyUpdate(BaseModel):
    policy_id: int = Field(..., gt=0, description="The policy ID must be greater than zero")
    description: Optional[str] = None
    policy_type: Optional[str] = None
