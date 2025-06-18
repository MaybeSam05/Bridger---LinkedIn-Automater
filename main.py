from playwright.async_api import async_playwright
import time
import pickle
import os
import re
import easyocr 
import base64
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import shutil
import sys
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
    directory = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
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
                # Wait for and fill in login form
                await page.wait_for_selector("#username")
                await page.fill("#username", username)
                await page.fill("#password", password)
                await page.click("button[type='submit']")
                
                # Wait for successful login
                await page.wait_for_url("https://www.linkedin.com/feed/", timeout=45000)
                print("✅ Successfully logged in!")
            except Exception as e:
                print(f"❌ Login failed: {str(e)}")
                return None
            
            print(f"Opening profile: {clientLink}")
            await page.goto(clientLink)
            
            # Create a unique directory name using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            directory = f"profile_{timestamp}"
            
            # Ensure we're in the correct directory
            base_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                
            directory = os.path.join(base_dir, directory)
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            
            print("📸 Taking screenshots of profile (this may take a few moments)...")
            
            # Hide right rail/sidebar and adjust content width
            await page.evaluate("""
                () => {
                    const rightRail = document.querySelector('.right-rail');
                    if (rightRail) rightRail.style.display = 'none';
                    
                    const asideElements = document.querySelectorAll('aside');
                    asideElements.forEach(el => el.style.display = 'none');
                    
                    const mainContent = document.querySelector('.body');
                    if (mainContent) mainContent.style.maxWidth = '800px';
                }
            """)
            
            time.sleep(1)

            print("Taking full page screenshot...")
            try:
                await page.screenshot(
                    path=f"{directory}/full_page.png",
                    full_page=True
                )
            except Exception as e:
                print(f"❌ Error in screenshot: {e}")
                return None
            
            print("✅ Screenshots processed")
            
            print("Converting profile to text...")
            txt = convertIMGtoTXT(f"{directory}/full_page.png")
            print("✅ Profile data extracted")
            
            return txt
            
    except Exception as e:
        print(f"❌ Error in clientProcess: {e}")
        return None
    finally:
        # Clean up screenshots directory if it exists
        if directory and os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                print(f"Error cleaning up directory: {e}")

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

def stitch_screenshots(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name) 

    images = []
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.png')],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )

    for file in files:
        img_path = os.path.join(folder_path, file)
        img = Image.open(img_path)
        
        crop_width = int(img.width * 0.7)
        cropped_img = img.crop((0, 0, crop_width, img.height))
        images.append(cropped_img)

    widths, heights = zip(*(img.size for img in images))
    total_height = sum(heights)
    max_width = max(widths)

    stitched_img = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for img in images:
        stitched_img.paste(img, (0, y_offset))
        y_offset += img.height

    output_path = os.path.join(folder_path, "stitched_screenshot.png")
    stitched_img.save(output_path)
    print(f"✅ Stitched screenshot saved")

    return output_path

async def take_screenshot(employee_link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print(f"Navigating to {employee_link}")
            await page.goto(employee_link)
            directory = employee_link.rstrip('/').split('/')[-1]
            
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            
            print("Waiting for page to load...")
            await page.wait_for_load_state('networkidle')
            
            print("Taking full page screenshot...")
            await page.screenshot(
                path=f"{directory}/full_page.png",
                full_page=True
            )
            

            '''
            # If we need multiple screenshots for some reason, we can still do that
            # Get page dimensions
            page_height = await page.evaluate("document.body.scrollHeight")
            viewport_height = await page.evaluate("window.innerHeight")
            print(f"Page height: {page_height}, Viewport height: {viewport_height}")
            
            if page_height > viewport_height:
                print("Taking additional screenshots for different viewport positions...")
                scroll_position = 0
                screenshot_num = 1
                
                while scroll_position < page_height:
                    # Wait for any animations to complete
                    await page.wait_for_load_state('networkidle')
                    
                    # Take screenshot of current viewport
                    await page.screenshot(
                        path=f"{directory}/screenshot_{screenshot_num}.png",
                        full_page=False
                    )
                    print(f"📸 Captured screenshot {screenshot_num}")
                    
                    # Scroll and increment
                    scroll_position += viewport_height
                    await page.evaluate(f"window.scrollTo(0, {scroll_position})")
                    screenshot_num += 1
            
            print(f"✅ Screenshots saved to {directory}")
            return directory
            '''
        except Exception as e:
            print(f"❌ Error in take_screenshot: {str(e)}")
            raise
        finally:
            await browser.close()

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

def convertIMGtoTXT(image_path):
    print("\nStarting OCR processing...")
    reader = easyocr.Reader(['en'], gpu=False) 
    results = reader.readtext(image_path)
    
    if not results:
        print("❌ No text was detected in the image!")
        return ''
        
    all_text = ' '.join(result[1] for result in results)
    
    cleaned_text = clean_ocr_text(all_text)
    
    if not cleaned_text:
        print("⚠️ Warning: Cleaned text is empty!")
    else:
        print(f"✅ Successfully extracted {len(cleaned_text)} characters of text")
        
    return cleaned_text

def clean_ocr_text(text):
    if len(text) > 850:
        original_length = len(text)
        cleaned = text[10:-30]
        cleaned_length = len(cleaned)
        print(f"\nText cleaning stats:")
        print(f"Original length: {original_length} characters")
        print(f"Cleaned length: {cleaned_length} characters")
        print(f"Removed {original_length - cleaned_length} characters")
        return cleaned
    else:
        print(f"\n⚠️ Text is too short ({len(text)} characters) to clean properly")
        return text