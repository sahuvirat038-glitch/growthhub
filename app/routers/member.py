from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from uuid import UUID
from app.models.space import Space
from app.auth.utils import get_current_user
from app.models.space_member import SpaceMember, Role
from app.schemas.space_member import SpaceMemberResponse


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)

@router.post("/{space_id}/join")
def join_space(space_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    space_exist = db.query(Space).filter(Space.id == space_id).first()
    if not space_exist :
        raise HTTPException(
            status_code=404,
            detail="Space not found"
        )
    already_joined = db.query(SpaceMember).filter(SpaceMember.space_id == space_id, SpaceMember.user_id == current_user.id).first()
    if already_joined:
        raise HTTPException(
            status_code=400,
            detail="Space already joined"
        )
    member_count = db.query(SpaceMember).filter(SpaceMember.space_id == space_id).count()
    if member_count >= space_exist.member_limit:
        raise HTTPException(
            status_code=400,
            detail="Space is full"
        )

    new_member = SpaceMember(
        user_id=current_user.id,
        space_id=space_id,
        role=Role.member
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {"message": "Successfully joined the space"}

@router.delete("/{space_id}/leave")
def leave_space(space_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    member = db.query(SpaceMember).filter(SpaceMember.space_id == space_id, SpaceMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=404, detail="You are not a member of this space")
    db.delete(member)
    db.commit()
    return {"message": "Successfully left the space"}

@router.get("/{space_id}/members", response_model=List[SpaceMemberResponse])
def get_members(space_id: UUID, db: Session = Depends(get_db)):
    all_member = db.query(SpaceMember).filter(SpaceMember.space_id == space_id).all()
    return all_member



