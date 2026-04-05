from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, AuthProvider
from app.auth.utils import create_access_token
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "https://web-production-5623.up.railway.app/auth/google/callback"

@router.get("/google")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return RedirectResponse(google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        userinfo_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = userinfo_response.json()

    email = user_info.get("email")
    name = user_info.get("name")
    avatar = user_info.get("picture")

    existing_user = db.query(User).filter(User.email == email).first()

    if not existing_user:
        new_user = User(
            username=name,
            email=email,
            avatar_url=avatar,
            provider=AuthProvider.google,
            password=None
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        existing_user = new_user

    jwt_token = create_access_token(data={"sub": existing_user.email})
    return RedirectResponse(f"http://localhost:5173/oauth?token={jwt_token}")