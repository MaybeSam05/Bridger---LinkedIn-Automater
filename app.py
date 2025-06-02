from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import main


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SetupRequest(BaseModel):
    link: str

class ConnectionRequest(BaseModel):
    link: str

class EmailRequest(BaseModel):
    address: str
    subject: str
    body: str

usertext = ""

@api.get("/")
def testing():
    return {"message": "API is running"}

@api.post("/authenticate_gmail")
def authenticate_gmail():
    gmail_service = main.authenticate_gmail()
    if gmail_service:
        return {"status": "authenticated"}
    else:
        raise HTTPException(status_code=500, detail="Failed to authenticate Gmail service")

@api.post("/setup")
def setup_profile(req: SetupRequest):
    if main.validLink(req.link):
        userTXT = main.saveCookies()
        usertext = userTXT # TEMPORARY GLOBAL VARIABLE REMOVE AFTER
        return {"status": "valid"}
    else:
        print("Invalid LinkedIn URL")
        raise HTTPException(status_code=400, detail="Invalid LinkedIn URL")

@api.post("/find_connection")
def find_connection(req: ConnectionRequest):
    if main.validLink(req.link):
        clientTXT = main.clientProcess(req.link)
        address, subject, body = main.generate_email(usertext, clientTXT)
        
        return {
            "status": "valid",
            "address": address,
            "subject": subject,
            "body": body
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid client URL")

@api.post("/send_email")
def send_email_endpoint(req: EmailRequest):
    success = main.send_email("me", req.address, req.subject, req.body)
    if success:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")
