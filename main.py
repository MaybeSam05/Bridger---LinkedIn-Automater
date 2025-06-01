from selenium import webdriver
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

def main():

    # PART 0:
    # authenticate_gmail

    #gmail_service = authenticate_gmail()

    # PART 1:
    # validLink, saveCookies

    #userTXT = saveCookies()
    #print(userTXT) 


    print("\n\n\n")
    # PART 2: 
    # validLink, clientProcess, generateEmail

    #clientTXT = clientProcess(clientLink)
    #print(clientTXT)
    #address, subject, body = generate_email(userTXT, clientTXT)

    #print("\n\n\n")

    # PART 3:
    # send_email

    #send_email(gmail_service, "me", address, subject, body)

def saveCookies(): 
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    print("You have 30 seconds to log in")
    time.sleep(30)

    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Cookies saved to linkedin_cookies.pkl")

    driver.quit()

    take_screenshot("https://www.linkedin.com/in/me/")
    outputPath = stitch_screenshots("me")
    txt = convertIMGtoTXT(outputPath)

    return txt

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
    time.sleep(5)

    page_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    scroll_position = 0
    screenshot_num = 1

    max_scrolls = page_height // viewport_height

    while scroll_position < page_height:
        driver.save_screenshot(f"{directory}/screenshot_{screenshot_num}.png")
        print(f"📸 Saved screenshot {screenshot_num}")

        scroll_position += viewport_height
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)

        screenshot_num += 1

    print(f"✅ {directory} fully captured")

    driver.quit()

    return directory

def generate_email(userTXT, clientTXT):
    
    messages = [
        {"role": "system", "content": "You're helping draft an email for a 15-minute coffee chat."},
        {"role": "user", "content": [
            {"type": "text", "text": f"You are a professional email assistant. I will give you two blocks of OCR-copied text from LinkedIn profiles: one from my own profile and one from the profile of a person I want to connect with. Your task is to: Analyze both profiles, Identify at least one genuine point of connection between us (this could be based on shared college/university, similar job roles, industries, locations, mutual interests, connections, organizations, or career paths), Compose a short, warm, professional email where I reach out to request a 15-minute virtual coffee chat. Guidelines: Be polite, conversational, and authentic. Mention the point of connection early to establish rapport. Include a clear ask for a short meeting (15-minute coffee chat) and offer flexibility. Keep it under 150 words. Do not fabricate shared details, only use what you can infer from the OCR data. I will paste two blocks of text below: Here is my Linkedin OCR data: {userTXT} and here is my connection's OCR data: {clientTXT}. RETURN ONLY connection's most likely email address, subject, and body. DO NOT RETURN ANYTHING ELSE, RETURN PLAIN TEXT ONLY, DO NOT ADD HEADERS. Return in this format: email//subject//body"},
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )

    email = response.choices[0].message.content

    address, subject, body = email.split("//")

    return address.strip(), subject.strip(), body.strip()

def validLink(url):
    pattern = r"^https:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$"

    if re.match(pattern, url):
        return True
    else:
        return False

def convertIMGtoTXT(image_path):
    reader = easyocr.Reader(['en']) 
    results = reader.readtext(image_path)
    
    all_text = ' '.join([result[1] for result in results])
    return all_text

if __name__ == "__main__":
    main()