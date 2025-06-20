from fastapi import FastAPI, HTTPException, Depends, Cookie, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import String
from pydantic import BaseModel
from datetime import datetime
import main
from database import get_db
import models
import json
import base64
from typing import Optional
from rate_limiter import rate_limit_dependency
import os
from jose import jwt, JWTError
import requests
from urllib.parse import urlencode

api = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://bridger.onrender.com/oauth/callback")

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bridger-8u91muc0s-samarth-vermas-projects-ac343338.vercel.app",
        "https://www.bridger-8u91muc0s-samarth-vermas-projects-ac343338.vercel.app",
        "https://bridger-eight.vercel.app",
        "https://bridger.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        #"http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Cookie"
    ],
    expose_headers=["Set-Cookie"],
    max_age=3600
)

class SetupRequest(BaseModel):
    link: str

class ConnectionRequest(BaseModel):
    link: str
    additional_context: str = ""  # Optional field with empty string default

class EmailRequest(BaseModel):
    address: str
    subject: str
    body: str

def get_current_user(Authorization: str = Header(...)):
    try:
        scheme, _, token = Authorization.partition(' ')
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("email")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_or_create_user(db: Session, user_email: str = None) -> models.User:
    """Get existing user by email or create a new one"""
    if user_email:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if user:
            user.last_login = datetime.now()
            db.commit()
            return user
    
    if not user_email:
        raise HTTPException(status_code=400, detail="Email address is required to create a new user")
        
    # Create new user if not found
    user = models.User(
        email=user_email,
        last_login=datetime.now(),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_user_session(db: Session, user: models.User) -> models.Session:
    """Create a new session for the user"""
    # Deactivate any existing active sessions
    db.query(models.Session).filter(
        models.Session.user_email == user.email,
        models.Session.is_active == True
    ).update({"is_active": False})
    
    session = models.Session(
        user_email=user.email,
        started_at=datetime.now(),
        last_active=datetime.now(),
        is_active=True
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@api.get("/")
def testing():
    return {"message": "API is running"}

@api.get("/health")
def health_check():
    """Health check endpoint that doesn't require database access"""
    try:
        # Check if database is available
        from database import engine
        if engine is not None:
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "degraded",
                "database": "not_available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api.post("/authenticate_gmail")
async def authenticate_gmail(request: Request, db: Session = Depends(get_db), _: bool = Depends(rate_limit_dependency)):
    try:
        
        gmail_service, user_email = main.authenticate_gmail()
        
        if not user_email:
            raise HTTPException(status_code=400, detail="Failed to get user email from Gmail")
        
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            user = models.User(
                email=user_email,
                last_login=datetime.now(),
                is_active=True
            )
            db.add(user)
        else:
            user.last_login = datetime.now()
            
        db.commit()
        db.refresh(user)
        
        try:
            with open('token.json', 'r') as token_file:
                token_data = json.load(token_file)
                expiry = token_data.get('expiry')
                if expiry:
                    try:
                        expiry_dt = datetime.fromtimestamp(float(expiry))
                    except (ValueError, TypeError):
                        try:
                            expiry_dt = datetime.fromisoformat(expiry.replace('Z', '+00:00'))
                        except (ValueError, AttributeError):
                            expiry_dt = None
                else:
                    expiry_dt = None

                user.gmail_token = token_data
                user.gmail_token_expiry = expiry_dt
                user.gmail_refresh_token = token_data.get('refresh_token', '')
                db.commit()
        except Exception as e:
            print(f"Error storing token: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to store Gmail token: {str(e)}")

        if gmail_service:
            # Issue JWT token
            token = jwt.encode({"email": user_email}, SECRET_KEY, algorithm="HS256")
            return {"status": "authenticated", "email": user_email, "token": token}
        else:
            raise HTTPException(status_code=500, detail="Failed to authenticate Gmail service")
    except Exception as e:
        print(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/setup")
async def setup_profile(
    request: Request,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_dependency),
    user_email: str = Depends(get_current_user)
):
    try:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")
        user = get_or_create_user(db, user.email)
        session = create_user_session(db, user)
        data = await request.json()
        linkedin_url = data.get("link")
        if not linkedin_url:
            raise HTTPException(status_code=400, detail="LinkedIn URL is required")
        # Process LinkedIn profile directly
        userTXT = await main.clientProcess(linkedin_url)
        if not userTXT:
            raise HTTPException(status_code=500, detail="Failed to capture LinkedIn profile")
        # Store userTXT in the User table
        user.usertxt = userTXT
        db.commit()
        return {
            "status": "valid",
            "email": user.email,
            "session_id": session.session_id
        }
    except Exception as e:
        print(f"Error in setup_profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/find_connection")
async def find_connection(
    request: Request,
    req: ConnectionRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_dependency),
    user_email: str = Depends(get_current_user)
):
    if not main.validLink(req.link):
        raise HTTPException(status_code=400, detail="Invalid client URL")
    try:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")
        if not user.usertxt:
            raise HTTPException(status_code=400, detail="User profile not found. Please set up your profile first.")
        # Process connection's profile
        clientTXT = await main.clientProcess(req.link)
        if not clientTXT:
            raise HTTPException(status_code=500, detail="Failed to process connection's profile")
        try:
            address, subject, body = main.generate_email(
                user.usertxt, 
                clientTXT,
                req.additional_context
            )
            return {
                "status": "valid",
                "address": address,
                "subject": subject,
                "body": body
            }
        except Exception as e:
            print(f"Error generating email: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate email: {str(e)}")
    except Exception as e:
        print(f"Error in find_connection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/send_email")
async def send_email_endpoint(
    request: Request,
    req: EmailRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_dependency),
    user_email: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")
    email = models.Email(
        user_email=user.email,
        email_address=req.address,
        subject=req.subject,
        body=req.body,
        status='pending'
    )
    db.add(email)
    db.commit()
    success = main.send_email(user.email, req.address, req.subject, req.body)
    email.status = 'sent' if success else 'failed'
    db.commit()
    if success:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

@api.get("/email_history")
async def get_email_history(
    request: Request,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_dependency),
    user_email: str = Depends(get_current_user)
):
    try:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")
        emails = db.query(models.Email).filter(
            models.Email.user_email == user.email
        ).order_by(models.Email.sent_at.desc()).all()
        email_list = []
        for email in emails:
            email_list.append({
                "sent_at": email.sent_at,
                "email_address": email.email_address,
                "subject": email.subject,
                "body": email.body,
                "status": email.status
            })
        return email_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/check_linkedin_status")
async def check_linkedin_status(
    request: Request,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_dependency),
    user_email: str = Depends(get_current_user)
):
    try:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            return {"has_user_profile": False}
        has_user_profile = user.usertxt is not None and user.usertxt.strip() != ""
        return {
            "has_user_profile": has_user_profile
        }
    except Exception as e:
        print(f"Error checking LinkedIn status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/oauth/url")
async def get_oauth_url():
    """Generate Google OAuth URL for frontend"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/userinfo.email openid',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    oauth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return {"oauth_url": oauth_url}

@api.get("/oauth/callback")
async def oauth_callback(code: str, db: Session = Depends(get_db)):
    """Handle OAuth callback from Google"""
    try:
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code is required")
        
        # Exchange code for tokens
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for tokens")
        
        tokens = response.json()
        
        # Get user info
        headers = {'Authorization': f"Bearer {tokens['access_token']}"}
        user_info_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        
        if user_info_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")
        
        user_info = user_info_response.json()
        user_email = user_info.get('email')
        
        if not user_email:
            raise HTTPException(status_code=400, detail="Email not found in user info")
        
        # Create or update user
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            user = models.User(
                email=user_email,
                last_login=datetime.now(),
                is_active=True
            )
            db.add(user)
        else:
            user.last_login = datetime.now()
        
        # Store tokens
        user.gmail_token = tokens
        user.gmail_token_expiry = datetime.fromtimestamp(tokens.get('expires_in', 0) + datetime.now().timestamp())
        user.gmail_refresh_token = tokens.get('refresh_token', '')
        
        db.commit()
        db.refresh(user)
        
        # Generate JWT token
        token = jwt.encode({"email": user_email}, SECRET_KEY, algorithm="HS256")
        
        # Return HTML that closes popup and sends message to parent
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
        </head>
        <body>
            <script>
                // Send success message to parent window
                if (window.opener) {{
                    window.opener.postMessage({{
                        type: 'oauth-success',
                        email: '{user_email}',
                        token: '{token}'
                    }}, '*');
                    window.close();
                }} else {{
                    // Fallback if no opener
                    window.location.href = '/?auth=success';
                }}
            </script>
            <p>Authentication successful! You can close this window.</p>
        </body>
        </html>
        """
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Failed</title>
        </head>
        <body>
            <script>
                if (window.opener) {{
                    window.opener.postMessage({{
                        type: 'oauth-error',
                        error: '{str(e)}'
                    }}, '*');
                    window.close();
                }} else {{
                    window.location.href = '/?auth=error';
                }}
            </script>
            <p>Authentication failed: {str(e)}</p>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=error_html, status_code=400)