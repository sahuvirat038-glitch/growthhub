from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.message import Message
from datetime import datetime


def delete_expired_messages():
    db = SessionLocal()
    try:
        db.query(Message).filter(
            Message.expires_at != None,
            Message.expires_at < datetime.now()
        ).delete()
        db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_messages, 'interval', minutes=1)
