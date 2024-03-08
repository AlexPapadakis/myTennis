from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Match
from app.models import MatchCreate

router = APIRouter()


@router.get("/matches", response_model=list[MatchCreate])
def get_all_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).all()
    return matches


@router.get("/matches/{match_id}", response_model=MatchCreate)
def get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.match_id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@router.post("/matches", response_model=MatchCreate)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.put("/matches/{match_id}", response_model=MatchCreate)
def update_match(match_id: int, match: MatchCreate, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.match_id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    for field, value in match.model_dump().items():
        setattr(db_match, field, value)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.match_id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return {"message": "Match deleted"}
