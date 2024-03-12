from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Venue
from ..models import VenueCreate, VenueResponse, VenueUpdate
from ..database import get_db
from .auth import verify_token, admin_only, get_roles
from .error_handler import execute_query_and_handle_errors

router = APIRouter()


@router.get("/venues", response_model=list[VenueResponse], dependencies=[Depends(admin_only)])
def read_venues(db: Session = Depends(get_db)):
    venues = execute_query_and_handle_errors(lambda: db.query(Venue).all(), "Venues")
    return venues


@router.get("/venues/{venue_id}", response_model=VenueResponse)
def read_venue_by_id(venue_id: int, db: Session = Depends(get_db)):
    print("Reading venue with id:", venue_id, "...")
    venue = execute_query_and_handle_errors(lambda: db.query(Venue).filter(Venue.venue_id == venue_id).first(), "Venue")
    return venue


@router.post("/venues", response_model=VenueResponse)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    print("Creating venue...")
    db_venue = Venue(**venue.model_dump())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


@router.put("/venues/{venue_id}", response_model=VenueResponse)
def update_venue(venue_id: int, venue: VenueUpdate, db: Session = Depends(get_db)):
    print("Updating venue with id:", venue_id, "...")
    db_venue = execute_query_and_handle_errors(lambda: db.query(Venue).filter(Venue.venue_id == venue_id).first(), "Venue")
    for attr, value in venue.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_venue, attr, value)
    db.commit()
    db.refresh(db_venue)
    print("Venue updated successfully.")
    return db_venue


@router.delete("/venues/{venue_id}", dependencies=[Depends(admin_only)])
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    print("Deleting venue with id:", venue_id, "...")
    db_venue = execute_query_and_handle_errors(lambda: db.query(Venue).filter(Venue.venue_id == venue_id).first(), "Venue")
    db.delete(db_venue)
    db.commit()
    return {"message": "Venue deleted"}
