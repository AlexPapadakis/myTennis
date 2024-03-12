import datetime
from decimal import Decimal
import time
from pydantic import BaseModel, constr, EmailStr, Field, validator
from datetime import date
from typing import Optional
from pydantic import condecimal,root_validator
from datetime import time,datetime
from passlib.context import CryptContext
from abc import ABC

_pwd_context = CryptContext(schemes=["bcrypt"])

MAX_SETS_PER_MATCH = 5
MAX_GAMES_PER_SET = 7

class UserBase(BaseModel,ABC):
    id: Optional[int] = Field(None, gt=0, read_only=True)
    password: Optional[str] = Field(None, max_length=255)
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    real_name: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    birthday: Optional[date] = Field(None)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    photo_url: Optional[str] = Field(None, max_length=255)
    created_at: Optional[datetime] = Field(None, read_only=True)

    class Config:
        orm_mode = True
        
class UserWithValidatorsBase(UserBase, ABC):

    @root_validator(pre=True)
    def hash_password(cls, values):
        password = values.get('password')
        if password:
            values['password'] = _pwd_context.hash(password)
        return values

    @validator('gender')
    def validate_gender(cls, value):
        print(f"Validating gender: {value}")
        valid_genders = ['Male', 'Female', 'Other']
        if value is not None and value not in valid_genders:
            raise ValueError(f'Invalid gender. Must be one of: {", ".join(valid_genders)}')
        return value

class UserCreate(UserWithValidatorsBase):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., max_length=255)

class UserUpdate(UserWithValidatorsBase):
    pass
class UserResponse(UserBase):     
    pass
    
    
class AthleteBase(BaseModel,ABC):
    user_id: Optional[int] = Field(None, gt=0, read_only=True)
    handedness: Optional[str] = Field(None, max_length=20)
    height: Optional[Decimal] = Field(None, gt=0, le=999.99)
    weight: Optional[Decimal] = Field(None, gt=0, le=999.99)
    backhand_type: Optional[str] = Field(None, max_length=20)
    skill_level: Optional[str] = Field(None, max_length=20)
    points: Optional[int] = Field(None, ge=0)
    
    class Config:
        orm_mode = True
        
class AthleteWithValidators(AthleteBase,ABC):
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
    
class AthleteCreate(AthleteWithValidators):
    handedness: str = Field(..., max_length=20)
    height: Decimal = Field(..., gt=0, le=999.99)
    weight: Decimal = Field(..., gt=0, le=999.99)
    backhand_type: str = Field(..., max_length=20)
    skill_level: str = Field(..., max_length=20)
class AthleteUpdate(AthleteWithValidators):
    pass
class AthleteResponse(AthleteBase):
    pass
    
    
    
    
    
class VenueBase(BaseModel,ABC):
    venue_id: Optional[int] = Field(None, gt=0, read_only=True)
    venue_name: Optional[str] = Field(None, max_length=100)
    venue_city: Optional[str] = Field(None, max_length=100)
    venue_address: Optional[str] = Field(None, max_length=100)
    surface_type: Optional[str] = Field(None, max_length=10)
    google_maps_url: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=255)
    
    class Config:
        orm_mode = True
class VenueWithValidators(VenueBase,ABC):
    @validator('surface_type')
    def validate_surface_type(cls, value):
        valid_surface_types = ['Hard', 'Grass', 'Clay']
        if value not in valid_surface_types:
            raise ValueError(f'Invalid surface type. Must be one of: {", ".join(valid_surface_types)}')
        return value
class VenueCreate(VenueWithValidators):
    venue_city: str = Field(..., max_length=100)
    venue_address: str = Field(..., max_length=100)
    surface_type: str = Field(..., max_length=10)

class VenueUpdate(VenueWithValidators):
    pass

class VenueResponse(VenueBase):
    pass



class MatchBase(BaseModel,ABC):
    match_id: Optional[int] = Field(None, gt=0,read_only=True)
    match_date: Optional[date] = Field(None)
    venue_id: Optional[int] = Field(None, gt=0)
    state: Optional[str] = Field(None, max_length=20)
    winner_id: Optional[int] = Field(None, gt=0)
    player1_id: Optional[int] = Field(None, gt=0)
    player2_id: Optional[int] = Field(None, gt=0)

    class Config:
        orm_mode = True
        
class MatchWithValidators(MatchBase,ABC):
    @validator('match_date')
    def validate_date(cls, value):
        if value is not None and value < date.today():
            raise ValueError('Match date must be in the future')
        return value
   
class MatchCreate(MatchWithValidators):
    @validator('state')
    def validate_state(cls, v):
        return "Upcoming"
    
class MatchUpdate(MatchWithValidators):
    @validator('state')
    def validate_state(cls, value):
        valid_states = ['Upcoming', 'Completed']
        if value is not None and value not in valid_states:
            raise ValueError(f'Invalid state. Must be one of: {", ".join(valid_states)}')
        return value
    
class MatchResponse(MatchBase):
    pass



class MatchInvitationBase(BaseModel,ABC):
    invitation_id: Optional[int] = Field(None, gt=0, read_only=True)
    sender_id: Optional[int] = Field(None, gt=0)
    recipient_id: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)
    invitation_date: Optional[datetime] = Field(None, read_only=True)
    scheduled_date: Optional[date] = Field(None)
    scheduled_time: Optional[time] = Field(None) 
    venue_id: Optional[int] = Field(None, gt=0)

    class Config:
        orm_mode = True
        
class MatchInvitationWithValidators(MatchInvitationBase,ABC):
    @validator('status')
    def validate_status(cls, value):
        valid_statuses = ['Pending', 'Accepted', 'Completed']
        if value is not None and value not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return value
    
class MatchInvitationCreate(MatchInvitationWithValidators):
    status: str = 'Pending'
    invitation_date: datetime = datetime.now()
    
    @validator('invitation_date', pre=True, always=True)
    def default_invitation_date(cls, v):
        return datetime.now()
    @validator('status', pre=True, always=True)
    def default_status(cls, v):
        return 'Pending'
    
class MatchInvitationUpdate(MatchInvitationWithValidators):
    @validator('status')
    def validate_status(cls, value):
        valid_statuses = ['Pending', 'Accepted', 'Completed']
        if value is not None and value not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return value


class MatchInvitationResponse(MatchInvitationBase):
    pass
    
    
    
    
    
    
    
    
    
class MatchScoreBase(BaseModel,ABC):
    match_id: Optional[int] = Field(None, gt=0)
    athlete_user_id: Optional[int] = Field(None, gt=0)
    set_number: Optional[int] = Field(None, gt=1)
    games_won: Optional[int] = Field(None, ge=0)
    class Config:
        orm_mode = True
        
class MatchScoreWithValidators(MatchScoreBase,ABC):
    @validator('set_number')
    def validate_set_number(cls, value):
        if value is not None and value > MAX_SETS_PER_MATCH:
            raise ValueError('Set number must not be greater than {MAX_SETS_PER_MATCH}')
        return value
    @validator('games_won')
    def validate_games_won(cls, value):
        if value is not None and value > MAX_GAMES_PER_SET:
            raise ValueError('Games won must be less or equal than {MAX_GAMES_PER_SET}')
        return value

class MatchScoreCreate(MatchScoreWithValidators):
    pass
class MatchScoreUpdate(MatchScoreWithValidators):
    pass
class MatchScoreResponse(MatchScoreBase):
    pass
        
