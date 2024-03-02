from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import User
from ..database import get_db

router = APIRouter()
        
@router.get("/home/")
def read_root():
    return {"Hello": "World"}


@router.get("/users/")
def read_user(db: Session = Depends(get_db)):
    print("Reading users...")
    users = db.query(User).all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return {"users": users}


