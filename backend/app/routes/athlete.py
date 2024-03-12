from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Athlete
from ..database import get_db
from ..models import AthleteCreate,AthleteResponse,AthleteUpdate
from .auth import verify_token, admin_only, get_roles
from .error_handler import execute_query_and_handle_errors

router = APIRouter()


@router.get("/athletes/", response_model=list[AthleteResponse], dependencies=[Depends(admin_only)])
def read_athletes(db: Session = Depends(get_db)):
    athletes = execute_query_and_handle_errors(lambda: db.query(Athlete).all(), "Athletes")
    return athletes


@router.get("/athletes/{user_id}", response_model=AthleteResponse)
def read_athlete_by_id(user_id: int, db: Session = Depends(get_db)):
    print("Reading athlete with id: ", user_id, "...")
    athlete = execute_query_and_handle_errors(lambda: db.query(Athlete).filter(Athlete.user_id == user_id).first(), "Athlete")
    return athlete


@router.post("/athletes/", response_model=AthleteResponse)
def create_athlete(athlete: AthleteCreate, db: Session = Depends(get_db)):
    print("Creating athlete...")
    db_athlete = Athlete(**athlete.model_dump())
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete


@router.put("/athletes/{user_id}", response_model=AthleteResponse)
def update_athlete(user_id: int, athlete: AthleteUpdate, db: Session = Depends(get_db)):
    print("Updating athlete with id: ", user_id, "...")

    db_athlete = execute_query_and_handle_errors(lambda: db.query(Athlete).filter(Athlete.user_id == user_id).first(), "Athlete")

    for attr, value in athlete.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_athlete, attr, value)
    db.commit()
    db.refresh(db_athlete)

    print("Athlete updated successfully.")

    return db_athlete


@router.delete("/athletes/{user_id}")
def delete_athlete(user_id: int, db: Session = Depends(get_db)):
    print("Deleting athlete with id: ", user_id, "...")
    athlete = execute_query_and_handle_errors(lambda: db.query(Athlete).filter(Athlete.user_id == user_id).first(), "Athlete")
    db.delete(athlete)
    db.commit()
    return {"message": "Athlete deleted"}
