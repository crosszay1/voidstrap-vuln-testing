import undetected_chromedriver as uc
import logging

def main():
    print("Starting Chrome...", flush=True)

    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, headless=False)
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.debug("Loading login page...", flush=True)
        driver.get("https://voidstrapp.pages.dev/pages/login")
        logging.info("Page title:", driver.title, flush=True)
        input("Press Enter to close...")
    finally:
        print("Closing Chrome...", flush=True)
        driver.quit()


if __name__ == "__main__":
    main()
