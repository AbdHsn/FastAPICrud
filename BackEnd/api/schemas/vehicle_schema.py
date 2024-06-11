from typing import List, Optional
from pydantic import BaseModel, Field, conlist, constr
from datetime import datetime

class VehicleCreate(BaseModel):
    #vehicle_id: Optional[int] = Field(None, description="The ID of the vehicle, automatically generated.")
    vehicle_model_id: int = Field(..., description="The model ID of the vehicle, referencing the VehicleModels table.")
    vehicle_type_id: int = Field(..., description="The type ID of the vehicle, referencing the VehicleTypes table.")
    vehicle_color_id: Optional[int] = Field(None, description="The color ID of the vehicle, referencing the VehicleColors table.")
    price_model_id: int = Field(..., description="The pricing model ID of the vehicle, referencing the PriceModels table.")
    title: str = Field(..., description="The title of the vehicle, often the model name and year.")
    description: str = Field(..., description="A description of the vehicle detailing features and other relevant information.")
    vin: str = Field(min_length=2) #constr(strip_whitespace=True, min_length=17, max_length=17) = Field(..., description="The Vehicle Identification Number, must be exactly 17 characters.")
    year: int = Field(..., description="The year of manufacture of the vehicle.")
    status: str = Field(min_length=2)#constr(strip_whitespace=True) = Field(..., description="The availability status of the vehicle.")
    images: Optional[str] #List[str] = Field(..., description="A list of image file names associated with the vehicle.")
    created_at: datetime = Field(..., description="The datetime when the vehicle record was created.")
    updated_at: Optional[datetime] = Field(None, description="The datetime when the vehicle record was last updated.")


class VehicleUpdate(BaseModel):
    vehicle_id: Optional[int] = Field(None, description="The ID of the vehicle, automatically generated.")
    vehicle_model_id: int = Field(..., description="The model ID of the vehicle, referencing the VehicleModels table.")
    vehicle_type_id: int = Field(..., description="The type ID of the vehicle, referencing the VehicleTypes table.")
    vehicle_color_id: Optional[int] = Field(None, description="The color ID of the vehicle, referencing the VehicleColors table.")
    price_model_id: int = Field(..., description="The pricing model ID of the vehicle, referencing the PriceModels table.")
    title: str = Field(..., description="The title of the vehicle, often the model name and year.")
    description: str = Field(..., description="A description of the vehicle detailing features and other relevant information.")
    vin: str = Field(min_length=2) #constr(strip_whitespace=True, min_length=17, max_length=17) = Field(..., description="The Vehicle Identification Number, must be exactly 17 characters.")
    year: int = Field(..., description="The year of manufacture of the vehicle.")
    status: str = Field(min_length=2)#constr(strip_whitespace=True) = Field(..., description="The availability status of the vehicle.")
    images: List[str] = Field(..., description="A list of image file names associated with the vehicle.")
    created_at: datetime = Field(..., description="The datetime when the vehicle record was created.")
    updated_at: Optional[datetime] = Field(None, description="The datetime when the vehicle record was last updated.")
