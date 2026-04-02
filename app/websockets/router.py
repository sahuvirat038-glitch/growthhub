from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import verify_token
from app.models.message import Message
from app.websockets.manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{channel_id}")
async def websocket_endpoint(channel_id: str, websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    email = verify_token(token)
    if email is None:
        await websocket.close(code=1008)
        return
    await manager.connect(channel_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(channel_id, f"{email}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(channel_id, websocket)

