from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
    # Chapter URLs
    chapter_urls = [
        {"name": "Chapter 1 District Governance", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOC%3a1"},
        {"name": "Chapter 2 Administration", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOC%3a2"},
        {"name": "Chapter 3 Business Operations", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOC%3a3"},
        {"name": "Chapter 4 Human Resources", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOC%3a4"},
        {"name": "Chapter 5 Students", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOC%3a5"},
        {"name": "Revision History", "url": "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=-2"},
    ]

    # Store scraped links
    scraped_links = []

    for chapter in chapter_urls:
        try:
            # Navigate to the chapter URL
            driver.get(chapter["url"])
            time.sleep(3)  # Wait for the page to load

            # Extract all links with "doJump" or other JavaScript calls
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "doJump" in href:
                    scraped_links.append({"chapter": chapter["name"], "link_text": link.text.strip(), "href": href})

            print(f"Scraped links from {chapter['name']}")

        except Exception as e:
            print(f"Error scraping {chapter['name']}: {e}")

    # Save results to a file
    with open("chapter_links.json", "w") as file:
        json.dump(scraped_links, file, indent=4)

    print(f"Scraped {len(scraped_links)} links successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
