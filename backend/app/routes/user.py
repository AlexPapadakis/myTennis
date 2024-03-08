from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import User
from ..database import get_db
from ..models import UserCreate

router = APIRouter()


@router.get("/users/", response_model=list[UserCreate])
def read_user(db: Session = Depends(get_db)):
    print("Reading users...")
    users = db.query(User).all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int, db: Session = Depends(get_db)):
    print("Reading user with id: ", user_id, "...")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("Creating user...")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user": db_user}

@router.put("/users/{user_id}", response_model=UserCreate)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    print("Updating user with id: ", user_id, "...")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for attr, value in user.model_dump().items():
        setattr(db_user, attr, value)
        
    db.commit()
    db.refresh(db_user)
    return {"user": db_user}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    print("Deleting user with id: ", user_id, "...")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"user": db_user}
