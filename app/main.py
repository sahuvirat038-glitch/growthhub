from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.routers.space import router as space_router
from app.routers.channel import router as channel_router
from app.routers.message import router as message_router
from app.websockets.router import router as ws_router
from app.routers.member import router as member_router
from starlette.middleware.sessions import SessionMiddleware
from app.auth.google import router as google_router
from app.auth.github import router as github_router
from dotenv import load_dotenv
from app.tasks import scheduler
from app.database import engine, Base
import app.models
import os

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.include_router(google_router)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()

app.include_router(auth_router)
app.include_router(space_router)
app.include_router(channel_router)
app.include_router(message_router)
app.include_router(ws_router)
app.include_router(member_router)
app.include_router(github_router)

@app.get("/")
def root():
    return {"message": "Welcome to the chat platform"}