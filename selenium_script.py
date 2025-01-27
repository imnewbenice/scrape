from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

# Specify paths to ChromeDriver and Chrome
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/google-chrome"

# Set up headless Chrome options
options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Path to the ChromeDriver
service = Service(CHROMEDRIVER_PATH)

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    url = "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOCView"
    driver.get(url)

    # Allow time for the page to load
    print("Waiting for page to load...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # Handle infinite scrolling (if applicable)
    print("Scrolling through the page to load all links...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust based on page load speed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all links on the page
    print("Extracting links...")
    links = driver.find_elements(By.TAG_NAME, "a")

    # Extract and filter URLs
    urls = list(set([link.get_attribute("href") for link in links if link.get_attribute("href")]))
    valid_urls = [url for url in urls if url.startswith("http")]

    # Save URLs to a JSON file
    print(f"Found {len(valid_urls)} valid URLs. Saving to file...")
    with open("scraped_urls.json", "w") as file:
        json.dump(valid_urls, file, indent=4)

    print("URLs successfully scraped and saved to scraped_urls.json")

except TimeoutException:
    print("Error: The page did not load within the expected time.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
