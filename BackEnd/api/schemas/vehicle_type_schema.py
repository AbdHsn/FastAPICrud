from pydantic import BaseModel, Field

class VehicleTypeCreate(BaseModel):
    name: str = Field(min_length=2)

class VehicleTypeUpdate(BaseModel):
    vehicle_type_id: int = Field(..., gt=0, description="The vehicle type ID must be greater than zero")
    name: str = Field(min_length=2)

