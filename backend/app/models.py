import datetime
from decimal import Decimal
import time
from pydantic import BaseModel, constr, EmailStr, Field, validator
from datetime import date
from typing import Optional
from pydantic import condecimal
from datetime import time,datetime


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
    
    
class AthleteCreate(BaseModel):
    user_id: int
    handedness: Optional[str] = Field(None, max_length=20)
    height: Optional[Decimal] = Field(None, gt=0, le=999.99)
    weight: Optional[Decimal] = Field(None, gt=0, le=999.99)
    backhand_type: Optional[str] = Field(None, max_length=20)
    skill_level: Optional[str] = Field(None, max_length=20)
    points: Optional[int]
    
    class Config:
        orm_mode = True
        
    @validator('handedness')
    def validate_handedness(cls, value):
        valid_handedness = ['Right-handed', 'Left-handed']
        if value is not None and value not in valid_handedness:
            raise ValueError(f'Invalid handedness. Must be one of: {", ".join(valid_handedness)}')
        return value
    
    @validator('backhand_type')
    def validate_backhand_type(cls, value):
        valid_backhand_types = ['One-handed', 'Two-handed']
        if value is not None and value not in valid_backhand_types:
            raise ValueError(f'Invalid backhand type. Must be one of: {", ".join(valid_backhand_types)}')
        return value
    
    @validator('skill_level')
    def validate_skill_level(cls, value):
        valid_skill_levels = ['Beginner', 'Intermediate', 'Advanced']
        if value is not None and value not in valid_skill_levels:
            raise ValueError(f'Invalid skill level. Must be one of: {", ".join(valid_skill_levels)}')
        return value
    
    
    
class VenueCreate(BaseModel):
    venue_name: str = Field(..., max_length=100)
    venue_city: str = Field(..., max_length=100)
    venue_address: str = Field(..., max_length=100)
    surface_type: str = Field(..., max_length=10)
    google_maps_url: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=255)
    
    class Config:
        orm_mode = True
        
    @validator('surface_type')
    def validate_surface_type(cls, value):
        valid_surface_types = ['Hard', 'Grass', 'Clay']
        if value not in valid_surface_types:
            raise ValueError(f'Invalid surface type. Must be one of: {", ".join(valid_surface_types)}')
        return value
    

class MatchCreate(BaseModel):
    date: Optional[date]
    venue_id: Optional[int]
    state: Optional[str] = Field(None, max_length=20)
    winner_id: Optional[int]
    player1_id: Optional[int]
    player2_id: Optional[int]
    
    class Config:
        orm_mode = True
        
    @validator('state')
    def validate_state(cls, value):
        valid_states = ['Upcoming', 'Completed']
        if value is not None and value not in valid_states:
            raise ValueError(f'Invalid state. Must be one of: {", ".join(valid_states)}')
        return value
    
    
    
    
class MatchInvitationCreate(BaseModel):
    invitation_id: Optional[int]
    sender_id: Optional[int]
    recipient_id: Optional[int]
    status: Optional[str] = Field(None, max_length=20)
    invitation_date: Optional[datetime]
    scheduled_date: Optional[date]
    scheduled_time: Optional[time]
    venue_id: Optional[int]

    class Config:
        orm_mode = True
        
    @validator('status')
    def validate_status(cls, value):
        valid_statuses = ['Pending', 'Accepted', 'Completed']
        if value is not None and value not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return value