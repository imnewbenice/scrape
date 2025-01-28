from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/google-chrome"

BASE_URL = "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs="

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

            # Extract all rows in the table containing policies or procedures
            rows = driver.find_elements(By.CSS_SELECTOR, "tr")
            for row in rows:
                try:
                    policy_number_element = row.find_element(By.CSS_SELECTOR, "td.PolNum a")
                    policy_title_element = row.find_element(By.CSS_SELECTOR, "td.PolTitle")
                    policy_type_element = row.find_element(By.CSS_SELECTOR, "td.PolType")

                    dojump_number = policy_number_element.get_attribute("href").split("(")[1].split(")")[0]
                    full_url = f"{BASE_URL}{dojump_number}"

                    policy_number = policy_number_element.text.strip()
                    policy_title = policy_title_element.text.strip()
                    policy_type = policy_type_element.text.strip()

                    # Remove the copyright symbol if present
                    policy_number = policy_number.replace("©", "").strip()

                    name = f"{policy_number} {policy_title} {policy_type}"

                    # Save the result
                    scraped_links.append({
                        "url": full_url,
                        "name": name,
                        "last_scraped": None,
                        "extract": "yes"
                    })
                except Exception as row_error:
                    print(f"Error processing row: {row_error}")

            print(f"Scraped links from {chapter['name']}")

        except Exception as e:
            print(f"Error scraping {chapter['name']}: {e}")

    # Save results to a file
    with open("urls.json", "w") as file:
        json.dump(scraped_links, file, indent=4, ensure_ascii=False)

    print(f"Scraped {len(scraped_links)} links successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
