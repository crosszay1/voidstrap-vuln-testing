import undetected_chromedriver as uc

driver = uc.Chrome()

try:
    driver.get("https://example.com")
    print("Page title:", driver.title)
    input("Press Enter to close...")
finally:
    driver.quit()