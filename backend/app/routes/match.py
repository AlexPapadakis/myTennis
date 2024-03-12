from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Match
from app.models import MatchCreate, MatchUpdate, MatchResponse
from app.routes.auth import verify_token, admin_only
from app.routes.error_handler import execute_query_and_handle_errors

router = APIRouter()


@router.get("/matches", response_model=list[MatchResponse])
def get_all_matches(db: Session = Depends(get_db)):
    matches = execute_query_and_handle_errors(lambda: db.query(Match).all(), "Matches")
    return matches


@router.get("/matches/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = execute_query_and_handle_errors(lambda: db.query(Match).filter(Match.match_id == match_id).first(), "Match")
    return match


@router.post("/matches", response_model=MatchResponse)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.put("/matches/{match_id}", response_model=MatchResponse)
def update_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = execute_query_and_handle_errors(lambda: db.query(Match).filter(Match.match_id == match_id).first(), "Match")
    for field, value in match.model_dump().items():
        if value is not None:
            setattr(db_match, field, value)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = execute_query_and_handle_errors(lambda: db.query(Match).filter(Match.match_id == match_id).first(), "Match")
    db.delete(db_match)
    db.commit()
    return {"message": "Match deleted"}
