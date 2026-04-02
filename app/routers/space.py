from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.utils import get_current_user
from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceResponse
from app.models.space_member import SpaceMember, Role


router = APIRouter(
    prefix="/space",
    tags=["Space"]
)


@router.post("/", response_model=SpaceResponse)
def create_space(space: SpaceCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
     if space.member_limit > 100:
         raise HTTPException(
             status_code = status.HTTP_400_BAD_REQUEST,
             detail = "Member limit cannot exceeded 100 "
         )

     new_space = Space(
         name = space.name,
         description = space.description,
         member_limit = space.member_limit,
         is_public = space.is_public,
         owner_id=current_user.id
     )

     db.add(new_space)
     db.commit()
     db.refresh(new_space)

     new_member = SpaceMember(
         user_id = current_user.id,
         space_id = new_space.id,
         role = Role.owner
     )

     db.add(new_member)
     db.commit()
     db.refresh(new_member)

     return new_space

@router.get("/", response_model=List[SpaceResponse])
def get_spaces(db: Session = Depends(get_db)):
    spaces = db.query(Space).filter(Space.is_public == True).all()
    return spaces


@router.get("/{space_id}", response_model=SpaceResponse)
def get_space(space_id: UUID, db: Session = Depends(get_db)):
    spaces = db.query(Space).filter(Space.id == space_id ).first()
    if not spaces:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Space not found"
        )
    return spaces