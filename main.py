from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

load_dotenv()

client = OpenAI()
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def saveCookies(): 
    driver = webdriver.Chrome()
    try:
        print("Opening LinkedIn login page...")
        driver.get("https://www.linkedin.com/login")
        max_wait_time = 45
        
        print("Please log in to LinkedIn...")
        
        wait = WebDriverWait(driver, max_wait_time)
        try:
            wait.until(lambda driver: "linkedin.com/feed" in driver.current_url)
            print("✅ Successfully logged in!")
        except:
            print("⚠️ Login timeout reached")
            return None, None
        
        print("Getting cookies...")
        cookies = driver.get_cookies()
        cookies_bytes = pickle.dumps(cookies)
        cookies_base64 = base64.b64encode(cookies_bytes).decode('utf-8')
        cookies_json = json.dumps({
            "cookie_data": cookies_base64,
            "created_at": datetime.now().isoformat()
        })
        print("✅ Cookies captured")
        
        print("Navigating to your profile...")
        # Navigate to user's profile using /me
        driver.get("https://www.linkedin.com/in/me/")
        time.sleep(2)  # Give time for redirect to actual profile
        
        # Get the actual profile URL after redirect
        actual_profile_url = driver.current_url
        print(f"✅ Found your profile at: {actual_profile_url}")
        
        # Create directory for screenshots
        directory = "me"  # Use consistent directory name for user profile
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.mkdir(directory)
        
        print("📸 Taking screenshots of your profile (this may take a few moments)...")
        # Take screenshots
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Set standard dimensions for consistent capture
        STANDARD_WIDTH = 850  # Reduced width to exclude sidebar
        STANDARD_HEIGHT = 800  # Standard viewport height
        
        # Set window size to our standard dimensions
        driver.set_window_size(STANDARD_WIDTH, STANDARD_HEIGHT)
        
        # Hide the right sidebar and adjust layout using JavaScript
        driver.execute_script("""
            // Hide right rail/sidebar
            const rightRail = document.querySelector('.right-rail');
            if (rightRail) rightRail.style.display = 'none';
            
            // Hide any other right-side elements
            const asideElements = document.querySelectorAll('aside');
            asideElements.forEach(el => el.style.display = 'none');
            
            // Adjust main content width
            const mainContent = document.querySelector('.body');
            if (mainContent) mainContent.style.maxWidth = '800px';
        """)
        
        # Wait for layout changes to take effect
        time.sleep(1)
        
        # Get page height after setting standard width and adjusting layout
        page_height = driver.execute_script("return document.body.scrollHeight")
        total_screenshots = (page_height + STANDARD_HEIGHT - 1) // STANDARD_HEIGHT

        scroll_position = 0
        screenshot_num = 1

        while scroll_position < page_height:
            wait.until(lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete")
            
            time.sleep(0.5)
            
            driver.save_screenshot(f"{directory}/screenshot_{screenshot_num}.png")
            print(f"📸 Capturing screenshot {screenshot_num}/{total_screenshots}")
            scroll_position += STANDARD_HEIGHT
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            screenshot_num += 1
        
        print("🔄 Processing screenshots...")
        # Stitch screenshots and convert to text
        outputPath = stitch_screenshots(directory)
        print("✅ Screenshots processed")
        
        print("Converting profile to text...")
        txt = convertIMGtoTXT(outputPath)
        print("✅ Profile data extracted")
        
        return txt, cookies_json
        
    except Exception as e:
        print(f"❌ Error in saveCookies: {e}")
        return None, None
    finally:
        print("Closing browser...")
        try:
            driver.quit()
        except:
            pass
        print("✅ Browser closed")

def clientProcess(clientLink, user_cookies_json=None):
    if not user_cookies_json:
        raise ValueError("LinkedIn cookies not provided")
        
    driver = webdriver.Chrome()
    try:
        print(f"Opening connection's profile: {clientLink}")
        driver.get(clientLink)
        
        print("Loading cookies from database...")
        # Decode and load cookies from database
        try:
            cookies_data = json.loads(user_cookies_json)
            cookie_bytes = base64.b64decode(cookies_data["cookie_data"])
            cookies = pickle.loads(cookie_bytes)
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            # Refresh to apply cookies
            driver.refresh()
            time.sleep(2)  # Give time for page to load
            print("✅ Cookies loaded")
        except Exception as e:
            print(f"❌ Error loading cookies: {e}")
            raise
        
        # Create directory for screenshots
        directory = clientLink.rstrip('/').split('/')[-1]
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.mkdir(directory)
        
        print("📸 Taking screenshots of connection's profile (this may take a few moments)...")
        # Take screenshots
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Set standard dimensions for consistent capture
        STANDARD_WIDTH = 850  # Reduced width to exclude sidebar
        STANDARD_HEIGHT = 800  # Standard viewport height
        
        # Set window size to our standard dimensions
        driver.set_window_size(STANDARD_WIDTH, STANDARD_HEIGHT)
        
        # Hide the right sidebar and adjust layout using JavaScript
        driver.execute_script("""
            // Hide right rail/sidebar
            const rightRail = document.querySelector('.right-rail');
            if (rightRail) rightRail.style.display = 'none';
            
            // Hide any other right-side elements
            const asideElements = document.querySelectorAll('aside');
            asideElements.forEach(el => el.style.display = 'none');
            
            // Adjust main content width
            const mainContent = document.querySelector('.body');
            if (mainContent) mainContent.style.maxWidth = '800px';
        """)
        
        # Wait for layout changes to take effect
        time.sleep(1)
        
        # Get page height after setting standard width and adjusting layout
        page_height = driver.execute_script("return document.body.scrollHeight")
        total_screenshots = (page_height + STANDARD_HEIGHT - 1) // STANDARD_HEIGHT

        scroll_position = 0
        screenshot_num = 1

        while scroll_position < page_height:
            wait.until(lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete")
            
            time.sleep(0.5)
            
            driver.save_screenshot(f"{directory}/screenshot_{screenshot_num}.png")
            print(f"📸 Capturing screenshot {screenshot_num}/{total_screenshots}")
            scroll_position += STANDARD_HEIGHT
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            screenshot_num += 1
        
        print("🔄 Processing screenshots...")
        # Stitch screenshots and convert to text
        outputPath = stitch_screenshots(directory)
        print("✅ Screenshots processed")
        
        print("Converting profile to text...")
        txt = convertIMGtoTXT(outputPath)
        print("✅ Profile data extracted")
        
        return txt
        
    except Exception as e:
        print(f"❌ Error in clientProcess: {e}")
        return None
    finally:
        print("Closing browser...")
        try:
            driver.quit()
        except:
            pass
        print("✅ Browser closed")

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
    
    # Get user's email address
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
        
        # Calculate the width to keep (70% of original width)
        crop_width = int(img.width * 0.7)
        
        # Crop the image to keep only the left 70%
        cropped_img = img.crop((0, 0, crop_width, img.height))
        images.append(cropped_img)

    # Get dimensions for the stitched image
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

def take_screenshot(employee_link):
    driver = webdriver.Chrome()
    try:
        driver.get(employee_link)
        directory = employee_link.rstrip('/').split('/')[-1]

        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.mkdir(directory)

        with open("linkedin_cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.refresh()
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        scroll_position = 0
        screenshot_num = 1

        while scroll_position < page_height:
            wait.until(lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete")
            
            time.sleep(0.5)
            
            driver.save_screenshot(f"{directory}/screenshot_{screenshot_num}.png")
            scroll_position += viewport_height
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            screenshot_num += 1

        return directory
    finally:
        driver.quit()

def structure_profile_data(text):
    print("\nStructuring profile data...")
    if not text:
        print("❌ No text provided to structure!")
        return "Error: No profile text to structure"
        
    location_pattern = re.compile(r'(?i)area|region|location')
    
    sections = {
        "name": "",
        "headline": "",
        "education": set(),
        "experience": set(),
        "location": "",
        "about": set(),
        "skills": set()
    }
    
    section_markers = {
        "education": {"education", "university", "college", "school"},
        "experience": {"experience", "work", "employment"},
        "skills": {"skills", "expertise", "technologies"},
        "about": {"about", "overview", "summary"}
    }
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    print(f"Found {len(lines)} non-empty lines to process")
    
    current_section = None
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if not sections["name"] and i < 5 and len(line.split()) <= 4:
            sections["name"] = line
            print(f"Found name: {line}")
            continue
            
        if not sections["headline"] and i < 7:
            if any(keyword in line_lower for keyword in {"student", "engineer", "developer"}):
                sections["headline"] = line
                print(f"Found headline: {line}")
                continue
        
        if not sections["location"] and location_pattern.search(line_lower):
            sections["location"] = line
            print(f"Found location: {line}")
            continue
            
        section_found = False
        for section, markers in section_markers.items():
            if any(marker in line_lower for marker in markers):
                current_section = section
                section_found = True
                print(f"\nFound {section} section")
                break
                
        if not section_found and current_section and len(line) > 3:
            sections[current_section].add(line)
    
    # Convert sets to lists
    for section in ["education", "experience", "skills", "about"]:
        sections[section] = list(sections[section])
        print(f"\n{section.capitalize()} items found: {len(sections[section])}")
    
    formatted_text = [
        f"Name: {sections['name']}",
        f"Headline: {sections['headline']}",
        f"Location: {sections['location']}",
        "",
        "About:",
        ' '.join(sections['about']) if sections['about'] else 'Not specified',
        "",
        "Education:",
        '\n'.join('- ' + edu for edu in sections['education']) if sections['education'] else 'Not specified',
        "",
        "Experience:",
        '\n'.join('- ' + exp for exp in sections['experience']) if sections['experience'] else 'Not specified',
        "",
        "Skills:",
        '\n'.join('- ' + skill for skill in sections['skills']) if sections['skills'] else 'Not specified'
    ]
    
    result = '\n'.join(formatted_text)
    print("\n✅ Profile structured successfully")
    print("\n📄 Structured Profile Preview:")
    print("-" * 50)
    preview_lines = result.split('\n')[:7]  # Show first 7 lines as preview
    print('\n'.join(preview_lines))
    print("...")
    print("-" * 50)
    
    return result

def generate_email(userTXT, clientTXT, additional_context=""):
    try:
        structured_user = structure_profile_data(userTXT)
        structured_client = structure_profile_data(clientTXT)
        
        context_prompt = ""
        if additional_context:
            context_prompt = f"\nAdditional Context Provided:\n{additional_context}\n\nPlease incorporate this context naturally into the email if relevant."
        
        messages = [
            {"role": "system", "content": "You're helping draft an email for a 15-minute coffee chat."},
            {"role": "user", "content": [
                {"type": "text", "text": f"""You are a professional email assistant. I will give you two structured LinkedIn profiles: mine and one from a person I want to connect with.

My LinkedIn Profile:
{structured_user}

Their LinkedIn Profile:
{structured_client}{context_prompt}

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
    
    # Print a sample of the detected text
    sample_length = 200
    text_sample = all_text[:sample_length] + "..." if len(all_text) > sample_length else all_text
    print("\n📄 Sample of detected text:")
    print("-" * 50)
    print(text_sample)
    print("-" * 50)
    
    cleaned_text = clean_ocr_text(all_text)
    
    if not cleaned_text:
        print("⚠️ Warning: Cleaned text is empty!")
    else:
        print(f"✅ Successfully extracted {len(cleaned_text)} characters of text")
        
    return cleaned_text

def clean_ocr_text(text):
    # Only clean the text if it's longer than 850 characters
    if len(text) > 850:
        # Keep track of original and cleaned lengths
        original_length = len(text)
        cleaned = text[150:-800]
        cleaned_length = len(cleaned)
        print(f"\nText cleaning stats:")
        print(f"Original length: {original_length} characters")
        print(f"Cleaned length: {cleaned_length} characters")
        print(f"Removed {original_length - cleaned_length} characters")
        return cleaned
    else:
        print(f"\n⚠️ Text is too short ({len(text)} characters) to clean properly")
        return text