from pydantic import BaseModel, Field
from typing import Optional

class PaymentGatewayCreate(BaseModel):
    name: str = Field(..., min_length=2)
    implementation_details: Optional[str] = None

class PaymentGatewayUpdate(BaseModel):
    gateway_id: int = Field(..., gt=0, description="The gateway ID must be greater than zero")
    name: Optional[str] = None
    implementation_details: Optional[str] = None
