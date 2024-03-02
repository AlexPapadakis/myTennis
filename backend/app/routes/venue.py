from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Venue
from ..database import get_db

router = APIRouter()

@router.get("/home/venue")
def read_root():
    return {"Hello": "venue"}


@router.get("/venues/")
def read_venue(db: Session = Depends(get_db)):
    print("Reading venues...")
    venues = db.query(Venue).all()
    if venues is None:
        raise HTTPException(status_code=404, detail="Venues not found")
    return {"Venues": venues}
