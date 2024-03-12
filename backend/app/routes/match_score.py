from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import MatchScore
from ..models import MatchScoreCreate, MatchScoreResponse, MatchScoreUpdate
from .error_handler import execute_query_and_handle_errors

router = APIRouter()


@router.get("/matchScores", response_model=list[MatchScoreResponse])
def get_all_match_scores(db: Session = Depends(get_db)):
    match_scores = execute_query_and_handle_errors(lambda: db.query(MatchScore).all(), "Match scores")
    return match_scores


@router.get("/matchScores/{athlete_user_id}/{match_id}/{set_number}", response_model=MatchScoreResponse)
def get_match_score(athlete_user_id: int, match_id: int, set_number: int, db: Session = Depends(get_db)):
    match_score = execute_query_and_handle_errors(lambda: db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first(), "Match score")
    
    return match_score
    


@router.get("/matchScores/{athlete_user_id}/{match_id}", response_model=list[MatchScoreResponse])
def get_match_scores_by_match(athlete_user_id: int, match_id: int, db: Session = Depends(get_db)):
    match_scores = execute_query_and_handle_errors(lambda: db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id
    ).all(), "Match scores")

    return match_scores
  


@router.post("/matchScores", response_model=MatchScoreResponse)
def create_match_score(match_score: MatchScoreCreate, db: Session = Depends(get_db)):
    db_match_score = MatchScore(**match_score.model_dump())
    db.add(db_match_score)
    db.commit()
    db.refresh(db_match_score)
    return db_match_score


@router.put("/matchScores/{athlete_user_id}/{match_id}/{set_number}", response_model=MatchScoreResponse)
def update_match_score(athlete_user_id: int, match_id: int, set_number: int, match_score: MatchScoreUpdate, db: Session = Depends(get_db)):
    db_match_score = execute_query_and_handle_errors(lambda: db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first(), "Match score")
 
    for attr, value in match_score.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_match_score, attr, value)
    db.commit()
    db.refresh(db_match_score)
    return db_match_score


@router.delete("/matchScores/{athlete_user_id}/{match_id}/{set_number}")
def delete_match_score(athlete_user_id: int, match_id: int, set_number: int, db: Session = Depends(get_db)):
    db_match_score = execute_query_and_handle_errors(lambda: db.query(MatchScore).filter(
        MatchScore.athlete_user_id == athlete_user_id,
        MatchScore.match_id == match_id,
        MatchScore.set_number == set_number
    ).first(), "Match score")
    
    db.delete(db_match_score)
    db.commit()
    return {"message": "Match score deleted successfully"}

