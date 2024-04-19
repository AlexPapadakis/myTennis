
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import TournamentCreate, TournamentUpdate, TournamentResponse
from app.schemas import Tournament
from app.routes.error_handler import execute_query_and_handle_errors

router = APIRouter()



@router.post("/tournaments", response_model=TournamentResponse)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    db_tournament = Tournament(**tournament.model_dump())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


@router.get("/tournaments/{tournament_id}", response_model=TournamentResponse)
def read_tournament_by_id(tournament_id: int, db: Session = Depends(get_db)):
    tournament = execute_query_and_handle_errors(lambda: db.query(Tournament).filter(Tournament.tournament_id == tournament_id).first(), "Tournament")
    return tournament


@router.get("/tournaments", response_model=list[TournamentResponse])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tournaments = execute_query_and_handle_errors(lambda: db.query(Tournament).offset(skip).limit(limit).all(), "Tournaments")
    return tournaments


@router.put("/tournaments/{tournament_id}", response_model=TournamentResponse)
def update_tournament(tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)):
    db_tournament = execute_query_and_handle_errors(lambda: db.query(Tournament).filter(Tournament.tournament_id == tournament_id).first(), "Tournament")
    for field, value in tournament.model_dump().items():
        if value is not None:
            setattr(db_tournament, field, value)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament



@router.delete("/tournaments/{tournament_id}", response_model=TournamentResponse)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    tournament = execute_query_and_handle_errors(lambda: db.query(Tournament).filter(Tournament.tournament_id == tournament_id).first(), "Tournament")
    db.delete(tournament)
    db.commit()
    return tournament

