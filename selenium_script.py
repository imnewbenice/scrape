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

    # Store scraped URLs
    scraped_data = []

    # Find all TOC buttons
    while True:
        # Refetch the TOC buttons in each loop to avoid stale element references
        buttons = driver.find_elements(By.CLASS_NAME, "TOCButton")
        for button in buttons:
            try:
                # Click the button
                button.click()
                time.sleep(3)  # Wait for the content to load

                # Scrape URLs from the new page
                links = driver.find_elements(By.TAG_NAME, "a")
                scraped_data.extend([link.get_attribute("href") for link in links if link.get_attribute("href")])

                # Go back to the main page and refetch buttons
                driver.back()
                time.sleep(2)
            except Exception as e:
                print(f"Error interacting with button: {e}")

        break  # End the loop after processing buttons

    # Save scraped data to a file
    with open("scraped_urls.json", "w") as file:
        json.dump(scraped_data, file, indent=4)

    print(f"Scraped {len(scraped_data)} URLs successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
