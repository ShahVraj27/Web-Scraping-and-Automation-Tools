import os
import time
import pandas as pd
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ---------------- Argument Parsing ----------------
parser = argparse.ArgumentParser(description="Scrapes tenders from Albania website and exports to Excel.")
parser.add_argument("--starting_page", type=int, required=True, help="Page number to start scraping from.")
parser.add_argument("--run_id", type=str, required=True, help="Unique run identifier.")
args = parser.parse_args()

# ---------------- Configuration ----------------
BASE_URL = 'https://www.app.gov.al/contract-notice'
COUNTRY = 'Albania'
WEBSITE_LINK = BASE_URL
starting_page = args.starting_page
run_id = args.run_id

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs", "Albania", run_id)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ---------------- WebDriver Setup ----------------
chromedriver_path = os.path.join(BASE_DIR, "edgedriver_win64", "msedgedriver.exe")
service = Service(executable_path=chromedriver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
driver.maximize_window()
driver.get(BASE_URL)

# ---------------- Helper Functions ----------------
def extract_tender_data():
    tenders = []
    tender_elements = driver.find_elements(By.CSS_SELECTOR, 'div.list-group-item-heading')
    for tender in tender_elements:
        try:
            title = tender.find_element(By.CSS_SELECTOR, 'div.col-lg-10').text.strip()#div.col-lg-10 strong span
            

            contracting_authority = tender.find_element(By.XPATH, ".//b[contains(text(), 'Contracting Authority:')]/following-sibling::span").text.strip()
            open_date = tender.find_element(By.XPATH, ".//b[contains(text(), 'Open Date:')]/following-sibling::span").text.strip()
            open_time = tender.find_element(By.XPATH, ".//b[contains(text(), 'Open Date:')]/following-sibling::small").text.strip()
            close_date = tender.find_element(By.XPATH, ".//b[contains(text(), 'Close Date:')]/following-sibling::span").text.strip()
            close_time = tender.find_element(By.XPATH, ".//b[contains(text(), 'Close Date:')]/following-sibling::small").text.strip()
            tender_number = tender.find_element(By.XPATH, ".//b[contains(text(), 'Tender Number:')]/following-sibling::span").text.strip()
            limit_fund = tender.find_element(By.XPATH, ".//b[contains(text(), 'Limit Fund:')]/following-sibling::span").text.strip()
            has_lots = tender.find_element(By.XPATH, ".//b[contains(text(), 'Has Lots:')]/following-sibling::span").text.strip()
            is_canceled = tender.find_element(By.XPATH, ".//b[contains(text(), 'Is Canceled:')]/following-sibling::span").text.strip()
            suspended = tender.find_element(By.XPATH, ".//b[contains(text(), 'Suspended:')]/following-sibling::span").text.strip()

            close_datetime_str = f"{close_date} {close_time}"
            close_datetime = datetime.strptime(close_datetime_str, '%d-%m-%Y %H:%M')

            if close_datetime >= datetime.now():
                tenders.append({
                    'Call For Tender': title,
                    #'Tender Description': description,
                    'Contracting Authority': contracting_authority,
                    'Open Date': f"{open_date} {open_time}",
                    'Close Date': close_datetime_str,
                    'Tender Number': tender_number,
                    'Limit Fund': limit_fund,
                    'Has Lots': has_lots,
                    'Is Canceled': is_canceled,
                    'Suspended': suspended,
                    'Country': COUNTRY,
                    'Website Link': WEBSITE_LINK
                })
        except (NoSuchElementException, ValueError):
            continue
    return tenders

def go_to_next_page():
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-default i.fa.fa-angle-right'))
        )
        driver.execute_script("arguments[0].click();", next_button)
        return True
    except (NoSuchElementException, TimeoutException):
        return False

# ---------------- Main Scraping Logic ----------------
# Skip to the starting page
current_page = 1
while current_page < starting_page:
    if not go_to_next_page():
        print(f"Failed to reach starting page: {starting_page}")
        driver.quit()
        exit()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.list-group-item-heading'))
    )
    current_page += 1
    time.sleep(2)

# Scrape from starting_page onward
while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.list-group-item-heading'))
        )
    except TimeoutException:
        print("Page content did not load in time.")
        break

    tenders = extract_tender_data()

    if tenders:
        df = pd.DataFrame(tenders)
        file_name = f'tenders_page_{current_page}.xlsx'
        output_file = os.path.join(OUTPUT_FOLDER, file_name)
        df.to_excel(output_file, index=False)
        print(f"Saved: {output_file}")

    if not go_to_next_page():
        break

    current_page += 1
    time.sleep(2)

driver.quit()
print("Scraping completed.")
