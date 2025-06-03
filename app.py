from fastapi import FastAPI, HTTPException, Depends, Cookie
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
import os
from dotenv import load_dotenv

load_dotenv()

api = FastAPI()

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

api.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

usertext = ""

def get_or_create_user(db: Session, linkedin_cookies: str = None, user_email: str = None) -> models.User:
    """Get existing user by email or LinkedIn cookies or create a new one"""
    if user_email:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if user:
            user.last_login = datetime.now()
            db.commit()
            return user
            
    if linkedin_cookies:
        try:
            # Parse the JSON-stored cookies
            cookies_json = json.loads(linkedin_cookies)
            user = db.query(models.User).filter(
                models.User.linkedin_cookies.cast(String).like(f'%{cookies_json["cookie_data"]}%')
            ).first()
            if user:
                user.last_login = datetime.now()
                db.commit()
                return user
        except (json.JSONDecodeError, KeyError):
            pass
    
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

@api.post("/authenticate_gmail")
def authenticate_gmail(db: Session = Depends(get_db)):
    try:
        # Get Gmail service and credentials
        gmail_service, user_email = main.authenticate_gmail()
        
        if not user_email:
            raise HTTPException(status_code=400, detail="Failed to get user email from Gmail")
        
        # Get or create user by email
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            user = models.User(
                email=user_email,
                last_login=datetime.now(),
                is_active=True
            )
            db.add(user)
        else:
            # Update last_login for existing user
            user.last_login = datetime.now()
            
        db.commit()
        db.refresh(user)
        
        # Read and store the token
        try:
            with open('token.json', 'r') as token_file:
                token_data = json.load(token_file)
                # Convert expiry from string to datetime if it exists
                expiry = token_data.get('expiry')
                if expiry:
                    try:
                        # Try parsing as timestamp first
                        expiry_dt = datetime.fromtimestamp(float(expiry))
                    except (ValueError, TypeError):
                        # If that fails, try parsing as ISO format
                        try:
                            expiry_dt = datetime.fromisoformat(expiry.replace('Z', '+00:00'))
                        except (ValueError, AttributeError):
                            # If all parsing fails, set to None
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
            return {"status": "authenticated", "email": user_email}
        else:
            raise HTTPException(status_code=500, detail="Failed to authenticate Gmail service")
    except Exception as e:
        print(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/setup")
def setup_profile(
    db: Session = Depends(get_db),
    linkedin_cookies: Optional[str] = Cookie(None)
):
    try:
        # Get or create user - we need the email from the previous Gmail authentication
        user = db.query(models.User).filter(
            models.User.gmail_token.is_not(None)
        ).order_by(models.User.last_login.desc()).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")
            
        user = get_or_create_user(db, linkedin_cookies, user.email)
        
        # Create new session
        session = create_user_session(db, user)
        
        # Save cookies and get profile text
        userTXT, cookies_json = main.saveCookies()
        if not userTXT or not cookies_json:
            raise HTTPException(status_code=500, detail="Failed to capture LinkedIn profile")
            
        # Update user's LinkedIn cookies directly from the saveCookies response
        user.linkedin_cookies = cookies_json
        db.commit()

        # Check if user already has a profile
        existing_profile = db.query(models.Profile).filter(
            models.Profile.user_email == user.email,
            models.Profile.is_user_profile == True
        ).first()

        if existing_profile:
            # Update existing profile
            existing_profile.raw_ocr_text = userTXT
            existing_profile.cleaned_text = main.clean_ocr_text(userTXT)
            existing_profile.last_scraped = datetime.now()
        else:
            # Create new profile
            profile = models.Profile(
                linkedin_url="https://www.linkedin.com/in/me/",
                raw_ocr_text=userTXT,
                cleaned_text=main.clean_ocr_text(userTXT),
                is_user_profile=True,
                user_email=user.email
            )
            db.add(profile)
        
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
def find_connection(req: ConnectionRequest, db: Session = Depends(get_db)):
    if not main.validLink(req.link):
        raise HTTPException(status_code=400, detail="Invalid client URL")

    try:
        # Get the most recent authenticated user
        user = db.query(models.User).filter(
            models.User.gmail_token.is_not(None)
        ).order_by(models.User.last_login.desc()).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")

        if not user.linkedin_cookies:
            raise HTTPException(status_code=400, detail="LinkedIn authentication required. Please set up your profile first.")

        # Get user's profile
        user_profile = db.query(models.Profile).filter(
            models.Profile.user_email == user.email,
            models.Profile.is_user_profile == True
        ).first()
        
        if not user_profile:
            raise HTTPException(status_code=400, detail="User profile not found. Please set up your profile first.")
        
        # Process connection's profile using cookies from database
        clientTXT = main.clientProcess(req.link, user.linkedin_cookies)
        if not clientTXT:
            raise HTTPException(status_code=500, detail="Failed to process connection's profile")

        # Get or create connection profile
        connection_profile = db.query(models.Profile).filter(
            models.Profile.user_email == user.email,
            models.Profile.linkedin_url == req.link,
            models.Profile.is_user_profile == False
        ).first()

        if connection_profile:
            # Update existing profile
            connection_profile.raw_ocr_text = clientTXT
            connection_profile.cleaned_text = main.clean_ocr_text(clientTXT)
            connection_profile.last_scraped = datetime.now()
        else:
            # Create new profile
            connection_profile = models.Profile(
                linkedin_url=req.link,
                raw_ocr_text=clientTXT,
                cleaned_text=main.clean_ocr_text(clientTXT),
                is_user_profile=False,
                user_email=user.email,
                last_scraped=datetime.now()
            )
            db.add(connection_profile)

        try:
            db.commit()
            db.refresh(connection_profile)

            # Generate email with additional context
            address, subject, body = main.generate_email(
                user_profile.cleaned_text, 
                connection_profile.cleaned_text,
                req.additional_context
            )
            
            return {
                "status": "valid",
                "address": address,
                "subject": subject,
                "body": body
            }
            
        except Exception as e:
            db.rollback()
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save connection profile: {str(e)}")
            
    except Exception as e:
        print(f"Error in find_connection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/send_email")
def send_email_endpoint(req: EmailRequest, db: Session = Depends(get_db)):
    # Get the most recent authenticated user
    user = db.query(models.User).filter(
        models.User.gmail_token.is_not(None)
    ).order_by(models.User.last_login.desc()).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")

    # Get the most recent connection profile
    connection_profile = db.query(models.Profile).filter(
        models.Profile.user_email == user.email,
        models.Profile.is_user_profile == False
    ).order_by(models.Profile.profile_id.desc()).first()

    # Create email record
    email = models.Email(
        user_email=user.email,
        target_profile_id=connection_profile.profile_id if connection_profile else None,
        email_address=req.address,
        subject=req.subject,
        body=req.body,
        status='pending'
    )
    db.add(email)
    db.commit()

    # Send email
    success = main.send_email("me", req.address, req.subject, req.body)
    
    # Update email status
    email.status = 'sent' if success else 'failed'
    db.commit()

    if success:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

@api.get("/email_history")
def get_email_history(db: Session = Depends(get_db)):
    try:
        # Get the most recent authenticated user
        user = db.query(models.User).filter(
            models.User.gmail_token.is_not(None)
        ).order_by(models.User.last_login.desc()).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Please authenticate with Gmail first")

        # Get all emails for this user
        emails = db.query(models.Email).filter(
            models.Email.user_email == user.email
        ).order_by(models.Email.sent_at.desc()).all()

        # Convert to list of dictionaries
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
def check_linkedin_status(db: Session = Depends(get_db)):
    try:
        # Get the most recent authenticated user
        user = db.query(models.User).filter(
            models.User.gmail_token.is_not(None)
        ).order_by(models.User.last_login.desc()).first()
        
        if not user:
            return {"has_linkedin_cookies": False}

        # Check if user has valid LinkedIn cookies
        has_cookies = user.linkedin_cookies is not None and len(user.linkedin_cookies) > 0
        
        return {"has_linkedin_cookies": has_cookies}
    except Exception as e:
        print(f"Error checking LinkedIn status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
