# Creation Date: 01/06/2022


import os
import sys
import pytz
import calendar
from time import sleep
from random import randint
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date
from webdriver_manager.chrome import ChromeDriverManager

# See selenium locally: http://localhost:4444/ui#/sessions


def setup(method: str = "local"):
    ''' Returns: Browser session. '''
    if method == "production":
        options = webdriver.FirefoxOptions()
        browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options)
    else:
        browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.implicitly_wait(5)
    return browser


def login(browser):
    ''' Purpose: Logs into LinkedIn via Selenium. '''
    username, password = os.getenv("USER"), os.getenv("PASS")
    browser.get('https://www.linkedin.com/login')
    sleep(randint(10, 20))
    username_input = browser.find_element(
        By.CSS_SELECTOR, "input[id='username']")
    password_input = browser.find_element(
        By.CSS_SELECTOR, "input[id='password']")
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    sleep(randint(40, 60))


def build_text():
    ''' Returns: Built LinkedIn headline string. '''
    current_time = datetime.now(pytz.timezone('Australia/Queensland'))
    hour = current_time.strftime("%I %p").replace(" ", "").lower().lstrip('0')
    day = calendar.day_name[current_time.weekday()]
    return f"It is {hour} {day} for me!"


def get_current(browser):
    ''' Purpose: Get current LinkedIn headline. '''
    browser.get(f'{os.getenv("URL")}edit/forms/intro/new/?profileFormEntryPoint=PROFILE_SECTION')
    sleep(randint(10, 20))
    biography_input = browser.find_element(
        By.CSS_SELECTOR, "input[id*='-headline']")
    return biography_input.get_attribute("value")


def calculate_end(session_days: int = 9):
    ''' Returns: Session restart date. '''
    return date.today() + timedelta(days=session_days)


def update_text(browser, current_text: str):
    ''' Purpose: If changed, update LinkedIn headline text. '''
    new_text = build_text()
    if current_text != new_text:
        browser.get(f'{os.getenv("URL")}edit/forms/intro/new/?profileFormEntryPoint=PROFILE_SECTION')
        biography_input = browser.find_element(
            By.CSS_SELECTOR, "input[id*='-headline']")
        biography_input.clear()
        biography_input.send_keys(new_text)
        update_button = browser.find_element(
            By.XPATH, "(//button[@type='button'])[1]")
        update_button.click()
        print(f"Updated text: {new_text} at {datetime.now()}")
    sleep(randint(30, 45))
    return new_text


if __name__ == "__main__":
    load_dotenv()
    fail = 0
    while fail <= 10:
        environment = sys.argv[1] if len(sys.argv) >= 2 else "local"
        print(f"Running as: {environment}")
        browser = setup(environment)
        try:
            login(browser)
            print("Login success!")
            current_text = get_current(browser)
            print(f"Current text: {current_text}")
            end_day = calculate_end()
            print(f"Session restarts: {end_day}")
            while True:
                day = date.today()
                if day == end_day:
                    print("Session expired, restarting")
                    browser.quit()
                    break
                current_text = update_text(browser, current_text)
                fail = 0
        except Exception as e:
            print(f"Failed: \n{e}")
            browser.quit()
            fail += 1
            sleep(randint(1200, 1300))
        except KeyboardInterrupt:
            browser.quit()
            break
