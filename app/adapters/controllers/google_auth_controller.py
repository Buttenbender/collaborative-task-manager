from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.adapters.controllers.dependencies import get_current_user
from app.domain.entities.user import User
import os
import json
import secrets
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])

code_verifiers = {}

def get_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)

def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode()

@router.get("/authorize")
def authorize(user_id: int, db: Session = Depends(get_db)):
    flow = get_flow()
    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    code_verifiers[str(user_id)] = code_verifier

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=str(user_id),
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    return RedirectResponse(authorization_url)

@router.get("/callback")
def callback(code: str, state: str, db: Session = Depends(get_db)):
    try:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        code_verifier = code_verifiers.pop(state, None)
        if not code_verifier:
            raise HTTPException(status_code=400, detail="Code verifier not found")

        flow = get_flow()
        flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        flow.fetch_token(code=code, code_verifier=code_verifier)

        credentials = flow.credentials
        token_data = json.dumps({
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
        })

        user_id = int(state)
        repository = MySQLUserRepository(db)
        user = repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.calendar_token = token_data
        repository.update(user)

        return {"message": "Google Calendar connected successfully!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))