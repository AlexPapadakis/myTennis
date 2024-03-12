from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import MatchInvitation
from ..database import get_db
from ..models import MatchInvitationCreate, MatchInvitationResponse, MatchInvitationUpdate
from .auth import verify_token, admin_only, get_roles
from .error_handler import execute_query_and_handle_errors

router = APIRouter()


@router.get("/matchInvitations", response_model=list[MatchInvitationResponse], dependencies=[Depends(admin_only)])
def read_match_invitations(db: Session = Depends(get_db)):
    match_invitations = execute_query_and_handle_errors(lambda: db.query(MatchInvitation).all(), "Match Invitations")
    return match_invitations


@router.get("/matchInvitations/{match_invitation_id}", response_model=MatchInvitationResponse)
def read_match_invitation_by_id(match_invitation_id: int, db: Session = Depends(get_db)):
    print("Reading match invitation with id: ", match_invitation_id, "...")
    match_invitation = execute_query_and_handle_errors(
        lambda: db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first(),
        "Match Invitation"
    )
    return match_invitation


@router.post("/matchInvitations", response_model=MatchInvitationResponse)
def create_match_invitation(match_invitation: MatchInvitationCreate, db: Session = Depends(get_db)):
    print("Creating match invitation...")
    db_match_invitation = MatchInvitation(**match_invitation.model_dump())
    db.add(db_match_invitation)
    db.commit()
    db.refresh(db_match_invitation)
    return db_match_invitation


@router.put("/matchInvitations/{match_invitation_id}", response_model=MatchInvitationResponse)
def update_match_invitation(match_invitation_id: int, match_invitation: MatchInvitationUpdate, db: Session = Depends(get_db)):
    print("Updating match invitation with id: ", match_invitation_id, "...")
    db_match_invitation = execute_query_and_handle_errors(
        lambda: db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first(),
        "Match Invitation"
    )
    for attr, value in match_invitation.model_dump().items():
        if attr is not None and value is not None:
            setattr(db_match_invitation, attr, value)
    db.commit()
    db.refresh(db_match_invitation)
    print("Match invitation updated successfully.")
    return db_match_invitation


@router.delete("/matchInvitations/{match_invitation_id}", dependencies=[Depends(admin_only)])
def delete_match_invitation(match_invitation_id: int, db: Session = Depends(get_db)):
    print("Deleting match invitation with id: ", match_invitation_id, "...")
    db_match_invitation = execute_query_and_handle_errors(
        lambda: db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first(),
        "Match Invitation"
    )
    db.delete(db_match_invitation)
    db.commit()
    
    return {"message": "Match invitation deleted"}