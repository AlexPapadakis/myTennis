from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Athlete
from ..models import AthleteCreate

router = APIRouter()

@router.get("/athletes", response_model=list[AthleteCreate])
def get_athletes(db: Session = Depends(get_db)):
    athletes = db.query(Athlete).all()
    if athletes is None:
        raise HTTPException(status_code=404, detail="Athletes not found")
    return athletes


@router.get("/athletes/{user_id}", response_model=AthleteCreate)
def get_athlete(user_id: int, db: Session = Depends(get_db)):
    athlete = db.query(Athlete).filter(Athlete.user_id == user_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete

@router.post("/athletes", response_model=AthleteCreate)
def create_athlete(athlete: AthleteCreate, db: Session = Depends(get_db)):
    new_athlete = Athlete(**athlete.model_dump())
    db.add(new_athlete)
    db.commit()
    db.refresh(new_athlete)
    return athlete

@router.put("/athletes/{user_id}", response_model=AthleteCreate)
def update_athlete(user_id: int, athlete: AthleteCreate, db: Session = Depends(get_db)):
    existing_athlete = db.query(Athlete).filter(Athlete.user_id == user_id).first()
    if not existing_athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    for attr, value in athlete.model_dump().items():
        setattr(existing_athlete, attr, value)
    db.commit()
    db.refresh(existing_athlete)
    return existing_athlete

@router.delete("/athletes/{user_id}")
def delete_athlete(user_id: int, db: Session = Depends(get_db)):
    athlete = db.query(Athlete).filter(Athlete.user_id == user_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    db.delete(athlete)
    db.commit()
    return {"message": "Athlete deleted"}
