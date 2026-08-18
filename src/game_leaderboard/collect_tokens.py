import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path

import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from game_leaderboard.smails_box import SmailsMailbox

logging.basicConfig(level=logging.DEBUG)

TOKENS_FILE = Path(__file__).parent / "tokens.txt"


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


def append_token(token: str) -> None:
    with TOKENS_FILE.open("a") as f:
        f.write(token + "\n")
    logging.info(f"Appended token to {TOKENS_FILE}")


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
        logging.debug("program still alive")


def main():
    for i in range(50):
        logging.info(f"Starting run {i + 1}/50")

        failures = 0

        while failures < 3:
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    token = executor.submit(worker).result(timeout=30)
                    if token:
                        append_token(token)
                    break

            except TimeoutError:
                logging.error(f"Run {i + 1}: Attempt timed out")
                failures += 1

            except Exception as e:
                logging.error(f"Run {i + 1}: Attempt failed: {e}")
                failures += 1

        if failures >= 3:
            logging.error(f"Run {i + 1} failed after 3 attempts")

    logging.info("Completed all 50 runs")


if __name__ == "__main__":
    main()
