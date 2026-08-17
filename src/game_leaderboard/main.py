import logging
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from game_leaderboard.smails_box import SmailsMailbox


def verify_email(email, code):
    url = "https://voidstrapp.pages.dev/api/auth/email/verify"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Referer": "https://voidstrapp.pages.dev/pages/login",
        "Origin": "https://voidstrapp.pages.dev",
    }

    payload = {
        "email": email,
        "code": code
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )

    return response.status_code, response.json()


def worker():
    print("Starting Chrome...", flush=True)

    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--start-maximized")

    mailbox = SmailsMailbox()

    driver = uc.Chrome(
        options=options,
        headless=False,
        version_main=151
    )

    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.debug("Loading login page...")
        driver.get("https://voidstrapp.pages.dev/pages/login")

        logging.info("Requesting mailbox")

        if not mailbox.create_mailbox():
            logging.critical("Mailbox creation failed")
            exit(1)

        logging.info(
            f"Created mailbox successfully. "
            f"Token: {mailbox.token} Email: {mailbox.email}"
        )

        email_input = driver.find_element(By.ID, "emailInput")

        driver.execute_script("""
            arguments[0].removeAttribute("disabled");
            arguments[0].removeAttribute("aria-disabled");
            arguments[0].classList.remove("pointer-events-none");
            arguments[0].classList.remove("opacity-40");
        """, email_input)

        email_input.send_keys(mailbox.email)

        logging.info(f"Entered email: {mailbox.email}")

        logging.info("Waiting for cloudflare captcha to finish. (5 seconds)")

        time.sleep(5)

        driver.find_element(By.ID, "emailSubmit").click()

        logging.info("Clicked submit button")

        for i in range(30):
            logging.info(f"Waiting for code... ({i+1}/30)")
            code = mailbox.get_code()
            if code:
                logging.info(f"Got code: {code}")
                break
            if i == 29:
                logging.critical("Failed to get code after 30 seconds")
                exit(1)
            time.sleep(2)

        status_code, email_result = verify_email(mailbox.email, code)

        logging.info(f"Email verification result: {email_result}")

        if email_result.get("ok"):
            token = email_result["token"]
            logging.info(f"Token: {token}")
            return token
        else:
            logging.error("Verification failed")

    finally:
        logging.info("Closing Chrome...")
        driver.quit()


def main():
    failures = 0

    while failures < 3:
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                return executor.submit(worker).result(timeout=30)

        except TimeoutError:
            logging.error("Attempt timed out")
            failures += 1

        except Exception as e:
            logging.error(f"Attempt failed: {e}")
            failures += 1

    raise Exception("Failed 3 consecutive attempts")


def game_vote(auth, universe_id=redacted, vote=1): #vibecoded, didn't feel like it
    url = "https://voidstrapp.pages.dev/api/gamevote"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth}",
        "Referer": f"https://voidstrapp.pages.dev/pages/place?id={universe_id}&name=parkour-reborn",
        "Origin": "https://voidstrapp.pages.dev",
    }

    payload = {
        "universeId": universe_id,
        "vote": vote
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text

if __name__ == "__main__":
    token = main()
    result = game_vote(token)
    print(f"Vote result: {result.status_code}")