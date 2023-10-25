from selenium.webdriver.common.by import By
from seleniumbase import SB
import os
from dotenv import load_dotenv
from time import sleep


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
with SB(uc=True) as driver:
    driver.get(
        "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow"
    )
    driver.type("#identifierId", "emelycamilo1727@gmail.com")
    driver.click("#identifierNext > div > button")

    driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", "Teamo1727")
    driver.click("#passwordNext > div > button")

    sleep(5)

    driver.get("https://bard.google.com/")
    try_bard_button = driver.find_element(By.CLASS_NAME, "gmat-mdc-button")
    try_bard_button.click()

    driver.save_cookies(name="cookies.json")

# rename cookies.json.txt to cookies.json
os.rename("./saved_cookies/cookies.json.txt", "./saved_cookies/cookies.json")
with open("./saved_cookies/cookies.json", "r") as f:
    cookies = f.read()
    for cookie in cookies[0]:
        print(cookie)
