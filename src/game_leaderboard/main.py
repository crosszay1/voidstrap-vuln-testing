import logging
import random
import string
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from game_leaderboard.smails_box import SmailsMailbox


def main():
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

        # Find the email input
        email_input = driver.find_element(By.ID, "emailInput")

        #Enable input bc it's disabled no clue why
        driver.execute_script("""
            arguments[0].removeAttribute("disabled");
            arguments[0].removeAttribute("aria-disabled");
            arguments[0].classList.remove("pointer-events-none");
            arguments[0].classList.remove("opacity-40");
        """, email_input)

        # Enter the mailbox email
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
            if i == 30:
                logging.critical("Failed to get code after 30 seconds")
                exit(1)
            time.sleep(2)

        driver.find_element(By.ID, "codeInput").send_keys(code)

        logging.info(f"Entered code: {code}")

        driver.find_element(By.ID, "codeSubmit").click()

        logging.info("Clicked submit button (email code)")

        username = ''.join(random.choices(string.ascii_letters, k=20))

        username = ''.join(random.choices(string.ascii_letters, k=20))
        logging.info(f"Generated random username: {username}")

        wait = WebDriverWait(driver, 15)

        name_input = wait.until(
            EC.visibility_of_element_located((By.ID, "nameInput"))
        )

        name_input.send_keys(username)
        logging.info(f"Entered username: {username}")

        name_next = wait.until(
            EC.element_to_be_clickable((By.ID, "nameNext"))
        )


        logging.debug(f"nameNext displayed: {name_next.is_displayed()}")
        logging.debug(f"nameNext enabled: {name_next.is_enabled()}")
        logging.debug(f"nameNext disabled attr: {name_next.get_attribute('disabled')}")
        logging.debug(f"nameNext outerHTML: {name_next.get_attribute('outerHTML')}")

        time.sleep(1)  # Wait a moment before clicking because otherwise it doesn't work tbh I don't fucking know

        name_next.click()
        logging.info("Clicked submit button (username)")

        avatar_done = wait.until(EC.element_to_be_clickable((By.ID, "avatarDone")))

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            avatar_done
        )

        avatar_done.click()

        logging.info("Clicked submit button (avatar)")
        input("Press Enter to close...")

    finally:
        logging.info("Closing Chrome...")
        driver.quit()


if __name__ == "__main__":
    main()