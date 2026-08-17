import undetected_chromedriver as uc
import logging
from game_leaderboard.smails_box import SmailsMailbox #our mailbox thing
from selenium.webdriver.common.by import By

def main():
    print("Starting Chrome...", flush=True)

    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--start-maximized")

    mailbox = SmailsMailbox()
    driver = uc.Chrome(options=options, headless=False, version_main=151) #Because cachy os repos only support this and like fuck I don't wanna fuck with getting the new one this is easier
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.debug("Loading login page...")
        driver.get("https://voidstrapp.pages.dev/pages/login")
        logging.info("Requesting mailbox")
        if not mailbox.create_mailbox():
            logging.critical("Mailbox creation failed")
            exit(1)
        logging.info(f"Created mailbox successfully. Token: {mailbox.token} Email: {mailbox.email}")

        input("enter to close")
    finally:
        logging.info("Closing Chrome...")
        driver.quit()


if __name__ == "__main__":
    main()
