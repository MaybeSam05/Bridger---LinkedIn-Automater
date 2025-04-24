from selenium import webdriver
import time
import pickle

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    print("You have 30 seconds to log in manually...")
    time.sleep(30)

    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Cookies saved to linkedin_cookies.pkl")
    driver.quit()

    take_screenshot()

def take_screenshot():
    driver = webdriver.Chrome()

    # Ask user for link to employee's LinkedIn profile
    #employee_link = ask_employee_link()

    employee_link = "https://www.linkedin.com/in/tavleen-singh2006/"

    driver.get(employee_link)

    with open("linkedin_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)
    driver.save_screenshot("screenshot.png")
    print("✅ Screenshot saved as screenshot.png")
    driver.quit()

def ask_employee_link():
    link = input("Enter the link to the employee's LinkedIn profile: ")
    return link.strip()

if __name__ == "__main__":
    main()