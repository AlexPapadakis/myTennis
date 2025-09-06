from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request,Response
from datetime import datetime, timedelta
from pydantic import EmailStr
from ..models import UserLogIn
from sqlalchemy.orm import Session
from ..database import get_db

from ..services.auth_service import authenticate_user, get_user_roles, create_access_token




router = APIRouter()


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
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email,"id":user.id,"roles":user_roles}, expires_delta=access_token_expires
    )
    response = JSONResponse(content={"user_id": user.id})

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", secure=False, httponly=True,samesite='Lax')
    
    return response

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(key="access_token", secure=False, httponly=True, samesite='Lax')
    return {"detail": "You have been logged out."}







