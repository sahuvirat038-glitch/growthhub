from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from uuid import UUID
from app.models.space import Space
from app.models.channel import Channel
from app.auth.utils import get_current_user
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.post("/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    channel_exist = db.query(Channel).filter(Channel.id == message.channel_id).first()
    if not channel_exist:
        raise HTTPException(status_code=404,
                            detail="Channel not found"
        )

    messages = Message(
        content = message.content,
        channel_id = message.channel_id,
        author_id=current_user.id,
        expires_at=message.expires_at
    )

    db.add(messages)
    db.commit()
    db.r
    return messages


@router.get("/{channel_id}", response_model=List[MessageResponse])
def get_history(channel_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.models.user import User
    messages = db.query(Message).filter(
        Message.channel_id == channel_id
    ).order_by(Message.created_at).all()

    result = []
    for msg in messages:
        user = db.query(User).filter(User.id == msg.author_id).first()
        msg_dict = {
            "id": msg.id,
            "content": msg.content,
            "channel_id": msg.channel_id,
            "author_id": msg.author_id,
            "author_email": user.email if user else None,
            "created_at": msg.created_at,
            "expires_at": msg.expires_at
        }
        result.append(msg_dict)
    return result
