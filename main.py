from selenium import webdriver
import time
import pickle
import os
import base64
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
userLink = "https://www.linkedin.com/in/krish-a-shah324/"

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    print("You have 30 seconds to log in")
    time.sleep(30)

    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Cookies saved to linkedin_cookies.pkl")
    driver.quit()

    directory = take_screenshot("https://www.linkedin.com/in/raghul-ravindranathan-15657b161/")
    stitch_screenshots(directory)
    directory = take_screenshot("https://www.linkedin.com/in/tavleen-singh2006/")
    stitch_screenshots(directory)
    directory = take_screenshot("https://www.linkedin.com/in/krish-a-shah324/")
    stitch_screenshots(directory)

    #generate_email(userLink, directory)

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

def ask_employee_link():
    link = input("Enter the link to the employee's LinkedIn profile: ")
    return link.strip()

def generate_email(userLink, image_dir):
    
    stitched_path = os.path.join(image_dir, "stitched_screenshot.png")

    with open(stitched_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode("utf-8")

    image_message = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{img_data}",
            "detail": "low"
        }
    }

    messages = [
        {"role": "system", "content": "You're helping draft an email for a 15-minute coffee chat."},
        {"role": "user", "content": [
            {"type": "text", "text": f"Here's a screenshot from someone's LinkedIn profile. Use it to help write an email asking for a short coffee chat. This is my LinkedIn profile: {userLink} . Try to find things in common and mention them in the email. Please include the phrase, 'I'm sure you're incredibly busy, but if you do have 15 minutes to connect, I'm free (and leave space for me to include times). If none of those work, just let me know what does and I'll make it work.' Return in format: '<subject>;<body>'"},
            image_message
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )

    email = response.choices[0].message.content
    print(email)

    # subject, body = email.split(";")
    # print("Subject:", subject)
    # print("Body:", body)

    #subject, body = email.split(";")

    #print("Subject:", subject)
    #print("Body:", body)

if __name__ == "__main__":
    main()