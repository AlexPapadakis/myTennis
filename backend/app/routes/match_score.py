from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import MatchScore
from ..models import MatchScoreCreate

router = APIRouter()


@router.get("/matchScores", response_model=list[MatchScoreCreate])
def get_all_match_scores(db: Session = Depends(get_db)):
    match_scores = db.query(MatchScore).all()
    return match_scores




@router.get("/matchScores/{athlete_user_id}/{match_id}/{set_number}", response_model=MatchScoreCreate)
def get_match_score(athlete_user_id: int, match_id: int, set_number: int, db: Session = Depends(get_db)):
    match_score = db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first()
    if match_score:
        return match_score
    else:
        raise HTTPException(status_code=404, detail="Match score not found")

@router.get("/matchScores/{athlete_user_id}/{match_id}", response_model=list[MatchScoreCreate])
def get_match_scores_by_match(athlete_user_id: int, match_id: int, db: Session = Depends(get_db)):
    match_scores = db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id
    ).all()
    if match_scores:
        return match_scores
    else:
        raise HTTPException(status_code=404, detail="Match scores not found")


##   NOT IN LINE WITH THE CREATION LOGIC ##
@router.post("/matchScores", response_model=MatchScoreCreate)
def create_match_score(match_score: MatchScoreCreate, db: Session = Depends(get_db)):
    db_match_score = MatchScore(**match_score.model_dump())
    db.add(db_match_score)
    db.commit()
    db.refresh(db_match_score)
    return db_match_score




@router.put("/matchScores/{athlete_user_id}/{match_id}/{set_number}", response_model=MatchScoreCreate)
def update_match_score(athlete_user_id: int, match_id: int, set_number: int, match_score: MatchScoreCreate, db: Session = Depends(get_db)):
    db_match_score = db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first()
    if db_match_score:
        for field, value in match_score.model_dump().items():
            setattr(db_match_score, field, value)
        db.commit()
        db.refresh(db_match_score)
        return db_match_score
    else:
        raise HTTPException(status_code=404, detail="Match score not found")


@router.delete("/matchScores/{athlete_user_id}/{match_id}/{set_number}")
def delete_match_score(athlete_user_id: int, match_id: int, set_number: int, db: Session = Depends(get_db)):
    db_match_score = db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first()
    if db_match_score:
        db.delete(db_match_score)
        db.commit()
        return {"message": "Match score deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Match score not found")
