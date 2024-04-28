from typing import List, Tuple
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import User
from ..database import get_db
from ..models import UserCreate,UserResponse,UserUpdate

from .auth import admin_only,verify_token


from .error_handler import execute_query_and_handle_errors



router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: Tuple[str, List[str], int] = Depends(verify_token), db: Session = Depends(get_db)):
    _, _, user_id = current_user
    user = execute_query_and_handle_errors(lambda: db.query(User).filter(User.id == user_id).first(), "User")
    return user

@router.put("/users/me" , response_model=UserResponse)
def update_user_me(user: UserUpdate, current_user: Tuple[str, List[str], int] = Depends(verify_token), db: Session = Depends(get_db)):
    _, _, user_id = current_user
    db_user = execute_query_and_handle_errors(lambda: db.query(User).filter(User.id == user_id).first(), "User")
    print(user)
    for attr, value in user.model_dump().items():
        if attr is not None and value is not None:
            print(attr, value)
            setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    
    print("User updated successfully.")
    
    return db_user




@router.get("/users/", response_model=list[UserResponse],dependencies =[Depends(admin_only)])
def read_users(db: Session = Depends(get_db)): 
    users = execute_query_and_handle_errors(lambda: db.query(User).all(), "Users")
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    print("Reading user with id: ", user_id, "...")
    user = execute_query_and_handle_errors(lambda: db.query(User).filter(User.id == user_id).first(), "User")
    return user

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("Creating user...")
    db_user = User(**user.model_dump()) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    print("Updating user with id: ", user_id, "...")
    
    db_user = execute_query_and_handle_errors(lambda: db.query(User).filter(User.id == user_id).first(), "User")
    
    for attr, value in user.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    
    print("User updated successfully.")
    
    return db_user


@router.delete("/users/{user_id}",dependencies=[Depends(admin_only)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    print("Deleting user with id: ", user_id, "...")
    db_user = execute_query_and_handle_errors(lambda: db.query(User).filter(User.id == user_id).first(), "User")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}