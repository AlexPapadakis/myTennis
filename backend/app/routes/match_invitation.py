from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MatchInvitation
from app.models import MatchInvitationCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MatchInvitation
from app.models import MatchInvitationCreate

router = APIRouter()


router = APIRouter()


@router.get("/matchInvitations")
def get_all_match_invitations(db: Session = Depends(get_db)):
    match_invitations = db.query(MatchInvitation).all()
    return match_invitations


@router.get("/matchInvitations/{match_invitation_id}")
def get_match_invitation(match_invitation_id: int, db: Session = Depends(get_db)):
    db_match_invitation = db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first()
    if not db_match_invitation:
        raise HTTPException(status_code=404, detail="Match invitation not found")
    return db_match_invitation

@router.post("/matchInvitations")
def create_match_invitation(match_invitation: MatchInvitationCreate, db: Session = Depends(get_db)):
    db_match_invitation = MatchInvitation(**match_invitation.model_dump())
    db.add(db_match_invitation)
    db.commit()
    db.refresh(db_match_invitation)
    return db_match_invitation


@router.put("/matchInvitations/{match_invitation_id}")
def update_match_invitation(match_invitation_id: int, match_invitation: MatchInvitationCreate, db: Session = Depends(get_db)):
    db_match_invitation = db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first()
    if not db_match_invitation:
        raise HTTPException(status_code=404, detail="Match invitation not found")
    for field, value in match_invitation.model_dump().items():
        setattr(db_match_invitation, field, value)
    db.commit()
    db.refresh(db_match_invitation)
    return db_match_invitation

@router.delete("/matchInvitations/{match_invitation_id}")
def delete_match_invitation(match_invitation_id: int, db: Session = Depends(get_db)):
    db_match_invitation = db.query(MatchInvitation).filter(MatchInvitation.invitation_id == match_invitation_id).first()
    if not db_match_invitation:
        raise HTTPException(status_code=404, detail="Match invitation not found")
    db.delete(db_match_invitation)
    db.commit()
    return {"message": "Match invitation deleted successfully"}