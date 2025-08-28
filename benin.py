import os
import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
geckodriver_path = os.path.join(BASE_DIR, "geckodriver.exe")

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
options.set_preference("detach", True)

service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://marches-publics.bj/appels-doffres?status=1")

# Set items per page to 10
mat_select_trigger = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#mat-select-0 .mat-select-trigger"))
)
mat_select_trigger.click()
option_10 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//mat-option//span[normalize-space()='10']"))
)
option_10.click()

WebDriverWait(driver, 20).until(
    lambda d: len(d.find_elements(By.TAG_NAME, "app-appel-offre-item")) > 0
)

start_page = int(input("Enter starting page number: "))

while True:
    try:
        print(f"Scraping page {start_page}...")
        time.sleep(2)

        tender_cards = driver.find_elements(By.TAG_NAME, "app-appel-offre-item")
        print("Found tender cards:", len(tender_cards))
        data = []

        for card in tender_cards:
            # Name of Work
            try:
                name_of_work = card.find_element(By.CSS_SELECTOR, "p.item-title").text.strip()
            except:
                name_of_work = ""

            # Closing Date (relative XPath)
            try:
                closing_date = card.find_element(
                    By.XPATH, ".//mat-card-header/div[2]/div[4]/div/div[2]"
                ).text.strip()
            except:
                closing_date = ""

            # Delay (relative XPath, convert to hours)
            try:
                delay_raw = card.find_element(
                    By.XPATH, ".//mat-card-header/div[2]/div[5]/div/div[2]"
                ).text.strip()
                match = re.search(r"(\d+)\s*jour", delay_raw)
                if match:
                    days = int(match.group(1))
                    delay = str(days * 24)
                else:
                    delay = delay_raw
            except:
                delay = ""

            # Ministry and Department (if present)
            try:
                ministry = card.find_element(
                    By.XPATH,
                    ".//div[.//div[text()='Autorité Contractante']]/div[@class='regular']"
                ).text.strip()
            except:
                ministry = ""

            # Document Link (if any)
            try:
                doc_link = card.find_element(By.CSS_SELECTOR, "a[target='_blank']").get_attribute("href")
            except:
                doc_link = ""

            item = {
                "Name of Work": name_of_work,
                "Ministry and Department": ministry,
                "Delay (hours)": delay,
                "Closing Date / Deadline": closing_date,
                "Country": "Benin",
                "Apply Mode": "Online",
                "Website Link": driver.current_url,
                "Document Link": doc_link,
            }
            data.append(item)

        if data:
            df = pd.DataFrame(data)
            file_path = os.path.join(BASE_DIR, f"tenders_page_{start_page}.xlsx")
            df.to_excel(file_path, index=False)
            print(f"Saved: {file_path}")
        else:
            print(f"No tenders found on page {start_page}. Skipping Excel save.")

        # Pagination: find the visible "Next" button
        next_btns = driver.find_elements(By.CSS_SELECTOR, "button.mat-paginator-navigation-next")
        next_btn = None
        for btn in next_btns:
            if btn.is_displayed() and btn.is_enabled():
                next_btn = btn
                break

        if not next_btn:
            print("Next button not found or disabled. Reached last page or no pagination.")
            break

        next_btn.click()
        start_page += 1

        WebDriverWait(driver, 20).until(
            lambda d: len(d.find_elements(By.TAG_NAME, "app-appel-offre-item")) > 0
        )
        time.sleep(1)

    except Exception as e:
        print(f"Error on page {start_page}: {e}")
        break

driver.quit()
