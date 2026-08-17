import undetected_chromedriver as uc
import logging
from game_leaderboard.smails_box import SmailsMailbox
from selenium.webdriver.common.by import By


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

        input("Press Enter to close...")

    finally:
        logging.info("Closing Chrome...")
        driver.quit()


if __name__ == "__main__":
    main()