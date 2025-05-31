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
    userTXT: str

class EmailRequest(BaseModel):
    #gmail_service: str
    address: str
    subject: str
    body: str

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
    if main.validlink(req.link):
        userTXT = main.savecookies(req.link)
        return {"status": "valid", "userTXT": userTXT}
    else:
        raise HTTPException(status_code=400, detail="Invalid LinkedIn URL")

@api.post("/find_connection")
def find_connection(req: ConnectionRequest):
    if main.validlink(req.link):
        clientTXT = main.clientProcess(req.link)
        address, subject, body = main.generate_email(req.userTXT, clientTXT)
        return {
            "status": "valid",
            "clientTXT": clientTXT,
            "address": address,
            "subject": subject,
            "body": body
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid client URL")

@api.post("/send_email")
def send_email_endpoint(req: EmailRequest):
    main.send_email(req.gmail_service, "me", req.address, req.subject, req.body) # CHANGE THIS LINE!!!
    return {"message": "Email sent successfully"}
