from pydantic import BaseModel, Field
from typing import Optional

class PriceModelCreate(BaseModel):
    price_model_id: int
    name: str = Field(..., min_length=2)
    description: Optional[str] = None
    price: float

class PriceModelUpdate(BaseModel):
    price_model_id: int = Field(..., gt=0, description="The price model ID must be greater than zero")
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
