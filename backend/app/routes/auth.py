from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from ..schemas import User,UserRoles,Roles
from ..models import UserCreate
from sqlalchemy.orm import Session
from ..database import get_db

from dotenv import load_dotenv
import os

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

router = APIRouter()

 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if not verify_password(user.password,password):
        return False
    return user

def get_user_roles(user: User, db: Session):
    roles = db.query(Roles).join(UserRoles).filter(UserRoles.user_id == user.id).all()
    roles_names = [role.name for role in roles]
    return roles_names
    
    
def verify_password(user_password:str ,password: str):
    if pwd_context.verify(password, user_password):
        print("Password verified")
        return True
    print("Password not verified")
    return False

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    print("Logging in...")
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_roles = get_user_roles(user, db)     
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username,"roles":user_roles}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: list = payload.get("roles")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username,roles
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

