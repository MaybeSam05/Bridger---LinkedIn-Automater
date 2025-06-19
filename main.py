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

load_dotenv()

client = OpenAI()
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

async def clientProcess(clientLink):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 850, 'height': 800}
            )
            page = await context.new_page()
            print("Opening LinkedIn login page...")
            await page.goto("https://www.linkedin.com/login")

            username = os.getenv("USERNAME")
            password = os.getenv("PASSWORD")

            print("Logging in automatically...")
            try:
                await page.wait_for_selector("#username", timeout=10000)
                await page.wait_for_timeout(2000)
                await page.fill("#username", username)
                await page.wait_for_timeout(1500)
                await page.fill("#password", password)
                await page.wait_for_timeout(2000)
                await page.click("button[type='submit']")
                await page.wait_for_url("https://www.linkedin.com/feed/", timeout=45000)
                print("✅ Successfully logged in!")
            except Exception as e:
                print(f"❌ Login failed: {str(e)}")
                return None

            print(f"Opening profile: {clientLink}")
            await page.goto(clientLink)
            await page.wait_for_timeout(1000)

            print("Extracting profile text...")
            await page.wait_for_timeout(1000)

            profile_text = await page.locator('.ZUMfuREyJUboAigOglxAGMXYsygQhCjWNs').inner_text()
            await page.wait_for_timeout(3000)
            deduped_text = dedupe_paragraphs(profile_text)
            final_cleaned_text = clean_profile_text(deduped_text)

            print("✅ Profile data extracted")
            return final_cleaned_text

    except Exception as e:
        print(f"❌ Error in clientProcess: {e}")
        return None


def clean_profile_text(raw_text: str) -> str:
    junk_phrases = {
        "Follow", "Show all", "Activity", "Recent posts", "Explore Premium profiles",
        "People you may know", "Message", "Connect", "More", "Companies", "Schools",
        "Show all companies", "Show all 11 skills", "LinkedIn News", "Contact info",
        "followers", "connections", "hasn't posted yet"
    }

    seen = set()
    cleaned_lines = []

    for line in raw_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Skip if already seen
        if line in seen:
            continue
        # Skip if it contains junk
        if any(junk.lower() in line.lower() for junk in junk_phrases):
            continue
        seen.add(line)
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def dedupe_paragraphs(raw_text: str) -> str:
    seen = set()
    cleaned = []

    # Split text into paragraphs based on two or more newlines
    paragraphs = re.split(r'\n{2,}', raw_text)

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para in seen:
            continue
        seen.add(para)
        cleaned.append(para)

    return '\n\n'.join(cleaned)

def authenticate_gmail():
    creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ Token refreshed silently.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
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
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return False

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                return False
        else:
            print("No valid credentials available")
            return False

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        sent_message = service.users().messages().send(userId=user_id, body={'raw': raw}).execute()
        print(f"✅ Email sent to {to_email} with subject: {subject}")
        return True
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