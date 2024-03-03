from pydantic import BaseModel, constr, EmailStr, Field, validator
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., max_length=255)
    real_name: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] 
    phone: Optional[str] = Field(None, max_length=20)
    birthday: Optional[date]
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    photo_url: Optional[str] = Field(None, max_length=255)
    
    class Config:
        orm_mode = True
    
    @validator('gender')
    def validate_gender(cls, value):
        valid_genders = ['Male', 'Female', 'Other']
        if value is not None and value not in valid_genders:
            raise ValueError(f'Invalid gender. Must be one of: {", ".join(valid_genders)}')
        return value