from playwright.async_api import async_playwright
import time
import os
import re
import base64
from openai import OpenAI
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import json
from datetime import datetime
from database import SessionLocal
import models
import requests
import asyncio
import sys
import os
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
import platform

load_dotenv()

client = OpenAI()
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

async def clientProcess(clientLink):
    try:
        options = ChromiumOptions()
        
        # Set Chrome binary location based on OS
        if platform.system() == "Darwin":  # macOS
            options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif platform.system() == "Linux":
            options.binary_location = "/usr/bin/google-chrome-stable"
        elif platform.system() == "Windows":
            options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        
        options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')

        async with Chrome(options=options) as browser:
            tab = await browser.start()
            print("Opening LinkedIn login page...")
            await tab.go_to("https://www.linkedin.com/login")
        
            print("Logging in automatically...")
            try:
                # Find login form elements using Pydoll's find method
                username_field = await tab.find(id='username')
                password_field = await tab.find(id='password')
                
                # Type credentials with realistic timing
                await username_field.type_text(os.getenv("USERNAME"), interval=0.15)
                await password_field.type_text(os.getenv("PASSWORD"), interval=0.15)

                # Find and click submit button
                submit_button = await tab.query('button[type="submit"]')
                await submit_button.click()

                '''
                # CHECK HERE IF URL IS https://www.linkedin.com/feed/
                current_url = await tab.execute_script('return window.location.href')
                url = current_url["result"]["result"]["value"]
                print("CURRENT URL: ", url)

                await asyncio.sleep(2)
                if url.startswith("https://www.linkedin.com/feed/"):
                    print("✅ Successfully logged in and redirected to feed!")
                else:
                    print(f"⚠️ Unexpected URL after login: {url}")
                    return None
                '''
                print("✅ Successfully logged in!")
            except Exception as e:
                print(f"❌ Login failed: {str(e)}")
                return None

            print(f"Opening profile: {clientLink}")
            await tab.go_to(clientLink)
            await asyncio.sleep(1)

            print("Extracting profile text...")
            await asyncio.sleep(1)

            profile_section = await tab.query('div#profile-content.extended.tetris.pv-profile-body-wrapper')
            profile_text = await profile_section.text
            await asyncio.sleep(1)

            final_cleaned_text = clean_linkedin_profile_text(profile_text)

            #print("CLEANED PROFILE: ", final_cleaned_text)
            print("✅ Profile data extracted")
            return final_cleaned_text

    except Exception as e:
        print(f"❌ Error in clientProcess: {e}")
        return None

def authenticate_gmail():
    creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ Token refreshed silently.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('c.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("✅ New login completed.")

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    
    try:
        oauth2_service = build('oauth2', 'v2', credentials=creds)
        user_info = oauth2_service.userinfo().get().execute()
        user_email = user_info.get('email')
        print(f"✅ Retrieved user email: {user_email}")
        return service, user_email
    except Exception as e:
        print(f"❌ Failed to get user email: {e}")
        return service, None

def send_email(user_id, to_email, subject, body):
    """Send email using OAuth tokens stored in database"""
    try:
        # Get user from database to access tokens
        
        db = SessionLocal()
        try:
            user = db.query(models.User).filter(models.User.email == user_id).first()
            if not user or not user.gmail_token:
                print("No valid Gmail tokens found for user")
                return False
            
            # Check if token is expired and refresh if needed
            if user.gmail_token_expiry and user.gmail_token_expiry < datetime.now():
                if user.gmail_refresh_token:
                    # Refresh the token
                    refresh_data = {
                        'client_id': os.getenv("GOOGLE_CLIENT_ID"),
                        'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
                        'refresh_token': user.gmail_refresh_token,
                        'grant_type': 'refresh_token'
                    }
                    
                    response = requests.post('https://oauth2.googleapis.com/token', data=refresh_data)
                    if response.status_code == 200:
                        new_tokens = response.json()
                        user.gmail_token = new_tokens
                        user.gmail_token_expiry = datetime.fromtimestamp(
                            new_tokens.get('expires_in', 0) + datetime.now().timestamp()
                        )
                        db.commit()
                    else:
                        print("Failed to refresh token")
                        return False
                else:
                    print("Token expired and no refresh token available")
                    return False
            
            # Use the access token to send email
            access_token = user.gmail_token.get('access_token')
            if not access_token:
                print("No access token available")
                return False
            
            # Create Gmail service with OAuth credentials
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            creds = Credentials(
                access_token,
                refresh_token=user.gmail_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv("GOOGLE_CLIENT_ID"),
                client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
            )
            
            service = build('gmail', 'v1', credentials=creds)
            
            # Create and send email
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            sent_message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
            print(f"✅ Email sent to {to_email} with subject: {subject}")
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def generate_email(userTXT, clientTXT, additional_context=""):
    try:

        context_prompt = ""
        if additional_context:
            context_prompt = f"\nAdditional Context Provided:\n{additional_context}\n\nPlease incorporate this context naturally into the email if relevant."
        
        messages = [
            {"role": "system", "content": "You're helping draft an email for a 15-minute coffee chat."},
            {"role": "user", "content": [
                {"type": "text", "text": f"""You are a professional email assistant. I will give you two LinkedIn profiles: mine and one from a person I want to connect with.

My LinkedIn Profile:
{userTXT}

Their LinkedIn Profile:
{clientTXT}{context_prompt}

Your task is to:
1. Analyze both profiles
2. Identify genuine points of connection (education, job roles, industries, locations, interests, etc.)
3. Compose a short, warm, professional email requesting a 15-minute virtual coffee chat
4. Be polite and authentic
5. Mention connections early to establish rapport
6. Keep it under 150 words
7. Only use information from the profiles and provided context

Return in this format ONLY:
email//subject//body"""}
            ]}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300
        )

        email = response.choices[0].message.content.strip()
        parts = email.split("//")

        address = ""
        subject = ""
        body = ""

        if len(parts) == 1:
            body = parts[0].strip()
        elif len(parts) == 2:
            subject = parts[0].strip()
            body = parts[1].strip()
        elif len(parts) >= 3:
            address = parts[0].strip()
            subject = parts[1].strip()
            body = parts[2].strip()

        return address, subject, body

    except Exception as e:
        print(f"Error generating email: {str(e)}")
        return "", "", ""

def validLink(url):
    pattern = re.compile(r"^https:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$")
    return bool(pattern.match(url))

def clean_linkedin_profile_text(raw_text: str) -> str:
    if "Status is online" in raw_text:
        raw_text = raw_text.replace("Status is online", "")    
    
    raw_text = raw_text[:-1550]
    
    # Normalize whitespace and remove extra spaces
    text = re.sub(r'\s+', ' ', raw_text.strip())
    
    # Remove common UI elements and boilerplate text
    ui_elements = [
        "Send profile in a message", "Save to PDF", "Saved items", "Activity", 
        "About this profile", "Add profile section", "Open to", "Enhance profile",
        "Resources", "Create a post", "Show all activity", "Show all companies", 
        "Show all", "Following", "Private to you", "Contact info", 
        "Your viewers also viewed", "People you may know", "You might like",
        "Pages for you", "LinkedIn News", "Profile language", "Public profile & URL",
        "View", "Connect", "Follow", "Get started", "Discover who's viewed your profile",
        "Start a post to increase engagement", "See how often you appear in search results",
        "Show all analytics", "Analytics", "Past 7 days", "You haven't posted yet",
        "Posts you share will be displayed here", "Tell non-profits", "you're interested in",
        "getting involved with your time and skills", "connections", "followers",
        "profile views", "post impressions", "search appearances", "From your school"
    ]
    
    for element in ui_elements:
        text = text.replace(element, '')
    
    # Remove duplicate content patterns
    text = re.sub(r'([^·]+)(?:\s*·\s*\1)+', r'\1', text)  # Remove repeated content with bullet separators
    text = re.sub(r'([^–]+)(?:\s*–\s*\1)+', r'\1', text)  # Remove repeated content with dash separators
    
    # Remove duplicate sentences
    sentences = text.split('.')
    unique_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in unique_sentences:
            unique_sentences.append(sentence)
    
    # Join back together
    cleaned_text = '. '.join(unique_sentences)
    
    # Clean up any remaining artifacts
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Normalize whitespace
    cleaned_text = re.sub(r'\(\s*\)', '', cleaned_text)  # Remove empty parentheses
    cleaned_text = re.sub(r'\.+', '.', cleaned_text)  # Remove multiple periods
    
    return cleaned_text