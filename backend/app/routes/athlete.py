from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Athlete,User
from ..database import get_db
from ..models import AthleteCreate,AthleteResponse,AthleteUpdate,UserResponse
from .auth import admin_only,get_id_from_token
from typing import List,Tuple, Optional
from .error_handler import execute_query_and_handle_errors


router = APIRouter()

@router.get("/athletes/me", response_model=AthleteResponse)
def read_athlete_me(current_user_id: int = Depends(get_id_from_token), db: Session = Depends(get_db)):
    user_id = current_user_id
    print("Reading athlete with id: ", user_id, "...")
    athlete = execute_query_and_handle_errors(lambda: db.query(Athlete).filter(Athlete.user_id == user_id).first(), "Athlete")
    return athlete


@router.post("/athletes/me", response_model=AthleteResponse)
def create_athlete_me(athlete: AthleteCreate, current_user_id: int = Depends(get_id_from_token), db: Session = Depends(get_db)):
    print("Creating athlete...")
    athlete_data = athlete.model_dump()
    athlete_data['user_id'] = current_user_id
    db_athlete = Athlete(**athlete_data)
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete


@router.put("/athletes/me", response_model=AthleteResponse)
def update_athlete_me(athlete: AthleteUpdate, current_user: Tuple[str, List[str], int] = Depends(get_id_from_token), db: Session = Depends(get_db)):
    _, _, user_id = current_user
    db_athlete = execute_query_and_handle_errors(lambda: db.query(Athlete).filter(Athlete.user_id == user_id).first(), "Athlete")
    for attr, value in athlete.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_athlete, attr, value)
    db.commit()
    db.refresh(db_athlete)
    print("Athlete updated successfully.")
    return db_athlete


#, dependencies=[Depends(admin_only)]
@router.get("/athletes/", response_model=list[AthleteResponse])
def read_athletes(db: Session = Depends(get_db), city: Optional[str] = None ,gender:Optional[str]=None, skill_level: Optional[str] = None):
    query = db.query(Athlete).join(User).filter(Athlete.user_id == User.id)
    if city:
        print("Reading athletes from city: ", city, "...")
        query = query.filter(User.city == city)
    if skill_level:
        print("Reading athletes with skill level: ", skill_level, "...")
        query = query.filter(Athlete.skill_level == skill_level)
    if gender:
        print("Reading athletes with gender: ",gender,"...")
        query = query.filter(User.gender==gender)

        
        
    athletes = execute_query_and_handle_errors(lambda: query.all(), "Athletes")
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
