from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Venue
from ..models import VenueCreate
from ..database import get_db

router = APIRouter()

@router.get("/venues", response_model=list[VenueCreate])
def get_venues(db: Session = Depends(get_db)):
    venues = db.query(Venue).all()
    if venues is None:
        raise HTTPException(status_code=404, detail="Venues not found")
    return venues


@router.get("/venues/{venue_id}", response_model=VenueCreate)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.post("/venues", response_model=VenueCreate)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    db_venue = Venue(**venue.model_dump())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

@router.put("/venues/{venue_id}", response_model=VenueCreate)
def update_venue(venue_id: int, venue: VenueCreate, db: Session = Depends(get_db)):
    db_venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
    if not db_venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    for field, value in venue.model_dump().items():
        setattr(db_venue, field, value)
    db.commit()
    db.refresh(db_venue)
    return db_venue

@router.delete("/venues/{venue_id}")
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
    if not db_venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    db.delete(db_venue)
    db.commit()
    
    return {"message": "Venue deleted"}
