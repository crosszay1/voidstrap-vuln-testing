import undetected_chromedriver as uc


def main():
    driver = uc.Chrome()

    try:
        driver.get("https://example.com")
        print("Page title:", driver.title)
        input("Press Enter to close...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()