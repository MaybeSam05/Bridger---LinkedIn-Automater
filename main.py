from selenium import webdriver
import time
import pickle
import os

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    print("You have 30 seconds to log in manually...")
    time.sleep(30)

    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Cookies saved to linkedin_cookies.pkl")
    driver.quit()

    take_screenshot("https://www.linkedin.com/in/tavleen-singh2006/")
    take_screenshot("https://www.linkedin.com/in/raghul-ravindranathan-15657b161?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app")

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

    # Get the page height
    page_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    scroll_position = 0
    screenshot_num = 1

    os.mkdir(directory)

    while scroll_position < page_height:
        driver.save_screenshot(f"{directory}/screenshot_{screenshot_num}.png")
        print(f"📸 Saved screenshot {screenshot_num}")

        scroll_position += viewport_height
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)

        screenshot_num += 1

    driver.quit()

def ask_employee_link():
    link = input("Enter the link to the employee's LinkedIn profile: ")
    return link.strip()

if __name__ == "__main__":
    main()