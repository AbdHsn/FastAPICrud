from pydantic import BaseModel, Field

class UserTypeCreate(BaseModel):
    name: str = Field(min_length=2)

class UserTypeUpdate(BaseModel):
    user_type_id: int = Field(..., gt=0, description="The user type ID must be greater than zero")
    name: str = Field(min_length=2)

