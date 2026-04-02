from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from uuid import UUID
from app.models.space import Space
from app.auth.utils import get_current_user
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelResponse



router = APIRouter(
    prefix="/channels",
    tags=["Channels"]
)

@router.post("/", response_model=ChannelResponse)
def create_channel(channel:ChannelCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    space_exist = db.query(Space).filter(Space.id == channel.space_id).first()
    if not space_exist:
        raise HTTPException(status_code=404,
                            detail="Space not found"
        )
    new_channel = Channel(
        name = channel.name,
        description = channel.description,
        space_id = channel.space_id,
    )

    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)

    return new_channel

@router.get("/space/{space_id}", response_model=List[ChannelResponse])
def get_channel(space_id: UUID, db: Session = Depends(get_db)):
    channel_exist = db.query(Channel).filter(Channel.space_id == space_id).all()
    if not channel_exist:
        raise HTTPException(status_code=404,
                            detail= "Space not found"
        )
    return channel_exist

@router.get("/detail/{channel_id}", response_model=ChannelResponse)
def single_channel(channel_id: UUID, db: Session = Depends(get_db)):
    channel_id_exist = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel_id_exist:
        raise HTTPException(status_code=404,
                            detail= "Channel not found")
    return channel_id_exist