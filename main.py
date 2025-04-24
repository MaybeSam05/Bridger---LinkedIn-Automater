from selenium import webdriver
import time
import pickle

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    print("You have 60 seconds to log in manually...")
    time.sleep(30)

    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Cookies saved to linkedin_cookies.pkl")
    driver.quit()


if __name__ == "__main__":
    main()