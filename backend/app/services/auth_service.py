from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import Request,Depends,status
from fastapi.exceptions import HTTPException


from ..schemas import User, UserRoles, Roles
from ..config import pwd_context, SECRET_KEY, ALGORITHM



def get_user_roles(user: User, db: Session):
    roles = db.query(Roles).join(UserRoles).filter(UserRoles.user_id == user.id).all()
    roles_names = [role.name for role in roles]
    return roles_names
    
    
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
    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    return token.replace("Bearer ", "")


def extract_token_data(token: str = Depends(get_token_from_cookie)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        roles: list = payload.get("roles")
        id: int = payload.get("id")
        if email is None:
            return None
        return email, roles, id
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
def get_id_from_token(token_data: tuple = Depends(extract_token_data)):
    if token_data is None:
        return None
    _, _, id = token_data
    return id

def check_admin_role(token_data: tuple = Depends(extract_token_data)):
    if token_data is None:
        return False
    _, roles, _ = token_data
    return "admin" in roles

