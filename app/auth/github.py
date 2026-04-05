from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, AuthProvider
from app.auth.utils import create_access_token
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "https://web-production-5623.up.railway.app/auth/github/callback"

@router.get("/github")
async def github_login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"  # GitHub authorization URL
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=user:email"  # GitHub scope
    )
    return RedirectResponse(github_auth_url)

@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",  # GitHub token URL
            json={
                "code": code,
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        userinfo_response = await client.get(
            "https://api.github.com/user",  # GitHub user info URL
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = userinfo_response.json()

    email = user_info.get("email") or f"{user_info.get('login')}@github.com"
    name = user_info.get("login")  # GitHub username field
    avatar = user_info.get("avatar_url")  # GitHub avatar field

    existing_user = db.query(User).filter(User.email == email).first()

    if not existing_user:
        new_user = User(
            username=name,
            email=email,
            avatar_url=avatar,
            provider=AuthProvider.github,  # correct provider
            password=None
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        existing_user = new_user

    jwt_token = create_access_token(data={"sub": existing_user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}