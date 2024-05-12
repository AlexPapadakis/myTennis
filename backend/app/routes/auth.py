from typing import Optional
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter, Request,Response
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from pydantic import EmailStr
from ..schemas import User,UserRoles,Roles
from ..models import UserCreate, UserLogIn
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

def get_user_roles(user: User, db: Session):
    roles = db.query(Roles).join(UserRoles).filter(UserRoles.user_id == user.id).all()
    roles_names = [role.name for role in roles]
    return roles_names
    
@router.post("/token")
def login_for_access_token(login_data: UserLogIn , db: Session = Depends(get_db)):

    user = authenticate_user(login_data.email, login_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_roles = get_user_roles(user, db)     
    print("User roles: ",user_roles)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email,"id":user.id,"roles":user_roles}, expires_delta=access_token_expires
    )
    response = JSONResponse(content={"user_id": user.id})

    print("Setting cookie")
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", secure=False, httponly=True,samesite='Lax')
    
    return response

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(key="access_token", secure=False, httponly=True, samesite='Lax')
    return {"message": "You have been logged out."}


def authenticate_user(email: EmailStr, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return False
    if not verify_password(user.password,password):
        return False
    return user

def verify_password(user_password:str ,password: str):
    if pwd_context.verify(password, user_password):
        print("Password verified")
        return True
    print("Password not verified")
    return False


    



def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_token_from_cookie(request: Request):
    print(request.headers) #prints nothing...
    token = request.cookies.get('access_token')
    print(f"Token from cookie: {token}")  # Print the token

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token.replace("Bearer ", "")

def verify_token(token: str = Depends(get_token_from_cookie)):
    try:
        print(f"Token to verify: {token}")  # Print the token to verify

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        roles: list = payload.get("roles")
        id: int = payload.get("id")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email,roles,id
    
    except JWTError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_roles_from_token(token_data: tuple = Depends(verify_token)):
    email, roles,id = token_data
    return roles

def get_id_from_token(token_data: tuple = Depends(verify_token)):
    email, roles,id = token_data
    return id

def admin_only(roles: list = Depends(get_roles_from_token)):
    if "admin" in roles:
        print("Admin access granted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
