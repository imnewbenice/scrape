from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Set up headless Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Path to the ChromeDriver (you can adjust this for GitHub Actions environment)
service = Service('/usr/local/bin/chromedriver')

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    url = "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOCView"
    driver.get(url)

    # Allow time for JavaScript to load or wait explicitly for elements
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # Find all links on the page
    links = driver.find_elements(By.TAG_NAME, "a")

    # Extract and print URLs
    urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    # Output the URLs
    with open("scraped_urls.txt", "w") as file:
        for url in urls:
            if url:
                file.write(url + "\n")

    print("URLs successfully scraped and saved to scraped_urls.txt")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
