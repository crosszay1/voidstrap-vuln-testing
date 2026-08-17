import undetected_chromedriver as uc
import logging

def main():
    print("Starting Chrome...", flush=True)

    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, headless=False, version_main=151) #Because cachy os repos only support this and like fuck I don't wanna fuck with getting the new one this is easier
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.debug("Loading login page...")
        driver.get("https://voidstrapp.pages.dev/pages/login")
        logging.info("Page title:", driver.title)
        input("Press Enter to close...")
    finally:
        logging.info("Closing Chrome...")
        driver.quit()


if __name__ == "__main__":
    main()
