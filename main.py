from selenium import webdriver
import time
import pickle
import os
import re
import easyocr
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import sys

load_dotenv()

client = OpenAI()
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    clientLink = "https://www.linkedin.com/in/sarah-benedicto/"

    #gmail_service = authenticate_gmail()

    # PART 1:
    # validLink, saveCookies

    userTXT = saveCookies()
    print(userTXT) 


    print("\n\n\n")
    # PART 2: 
    # validLink, clientProcess

    clientTXT = clientProcess(clientLink)
    print(clientTXT) 

    print("\n\n\n")

    # PART 3:
    # generateEmail, send_email

    address, subject, body = generate_email(userTXT, clientTXT)
    sys.exit()
    send_email(gmail_service, "me", address, subject, body)

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

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

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
    print(f"✅ Authenticated as {creds.id_token['email']}")
    return service

def send_email(service, user_id, to_email, subject, body):
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        sent_message = service.users().messages().send(userId=user_id, body={'raw': raw}).execute()
        print(f"✅ Email sent to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

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
    stop_scrolls = max_scrolls - 2  

    os.mkdir(directory)

    while scroll_position < page_height and screenshot_num <= stop_scrolls:
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
            {"type": "text", "text": f"Here's the text from someone's LinkedIn profile. Here: {clientTXT}. Use it to help write an email asking for a short coffee chat. Additionally return what you think is MOST LIKELY to be this user's email address. This is the text of my LinkedIn profile: {userTXT}. Try to find things in common and mention them in the email. Please include the phrase, 'I'm sure you're incredibly busy, but if you do have 15 minutes to connect, I'm free (and leave space for me to include times). If none of those work, just let me know what does and I'll make it work.' Return in format: 'email::subject::body'"},
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )

    email = response.choices[0].message.content

    address, subject, body = email.split("::")

    print("Address:", address.strip())
    print("Subject:", subject.strip())
    print("Body:", body.strip())

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