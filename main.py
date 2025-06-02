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

load_dotenv()

client = OpenAI()
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def saveCookies(): 
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.linkedin.com/login")
        max_wait_time = 45
        
        print("Please log in to LinkedIn...")
        
        wait = WebDriverWait(driver, max_wait_time)
        try:
            wait.until(lambda driver: "linkedin.com/feed" in driver.current_url)
            print("✅ Successfully logged in!")
        except:
            print("⚠️ Login timeout reached")
        
        with open("linkedin_cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("✅ Cookies saved to linkedin_cookies.pkl")
        
        driver.close()
        
        take_screenshot("https://www.linkedin.com/in/me/")
        outputPath = stitch_screenshots("me")
        txt = convertIMGtoTXT(outputPath)
        
        return txt
        
    finally:
        driver.quit()

def clientProcess(clientLink):
    directory = take_screenshot(clientLink)
    outputPath = stitch_screenshots(directory)
    txt = convertIMGtoTXT(outputPath)

    return txt

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
    return service

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
        images.append(img)

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
    current_section = None
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if not sections["name"] and i < 5 and len(line.split()) <= 4:
            sections["name"] = line
            continue
            
        if not sections["headline"] and i < 7:
            if any(keyword in line_lower for keyword in {"student", "engineer", "developer"}):
                sections["headline"] = line
                continue
        
        if not sections["location"] and location_pattern.search(line_lower):
            sections["location"] = line
            continue
            
        section_found = False
        for section, markers in section_markers.items():
            if any(marker in line_lower for marker in markers):
                current_section = section
                section_found = True
                break
                
        if not section_found and current_section and len(line) > 3:
            sections[current_section].add(line)
    
    for section in ["education", "experience", "skills", "about"]:
        sections[section] = list(sections[section])
    
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
    
    return '\n'.join(formatted_text)

def generate_email(userTXT, clientTXT):
    try:
        structured_user = structure_profile_data(userTXT)
        structured_client = structure_profile_data(clientTXT)
        
        messages = [
            {"role": "system", "content": "You're helping draft an email for a 15-minute coffee chat."},
            {"role": "user", "content": [
                {"type": "text", "text": f"""You are a professional email assistant. I will give you two structured LinkedIn profiles: mine and one from a person I want to connect with.

My LinkedIn Profile:
{structured_user}

Their LinkedIn Profile:
{structured_client}

Your task is to:
1. Analyze both profiles
2. Identify genuine points of connection (education, job roles, industries, locations, interests, etc.)
3. Compose a short, warm, professional email requesting a 15-minute virtual coffee chat
4. Be polite and authentic
5. Mention connections early to establish rapport
6. Keep it under 150 words
7. Only use information from the profiles

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

def clean_ocr_text(text):
    return text[150:-700] if len(text) > 850 else ''

def convertIMGtoTXT(image_path):
    reader = easyocr.Reader(['en'], gpu=False) 
    results = reader.readtext(image_path)
    all_text = ' '.join(result[1] for result in results)
    cleaned_text = clean_ocr_text(all_text)
    return cleaned_text