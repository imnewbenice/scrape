from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/google-chrome"

options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    driver.get("https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOCView")

    # Wait for the buttons to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "TOCButton"))
    )

    # Find all TOC buttons
    buttons = driver.find_elements(By.CLASS_NAME, "TOCButton")
    scraped_data = []

    for button in buttons:
        # Click the button
        button.click()
        time.sleep(3)  # Adjust for loading time

        # Scrape the resulting content (example: extract all links)
        links = driver.find_elements(By.TAG_NAME, "a")
        scraped_data.extend([link.get_attribute("href") for link in links if link.get_attribute("href")])

        # Go back to the main page
        driver.back()
        time.sleep(2)

    # Save scraped data to a file
    with open("scraped_urls.json", "w") as file:
        json.dump(scraped_data, file, indent=4)

    print(f"Scraped {len(scraped_data)} URLs successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
