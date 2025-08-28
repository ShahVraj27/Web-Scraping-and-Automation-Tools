



# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# import datetime
# from datetime import date
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from deep_translator import GoogleTranslator  # ✅ NEW

# BASE_URL = "https://gnumner.minfin.am"
# MAIN_URL = BASE_URL + "/en/page/announcement_and_invitation_of_an_open_tender/1"
# LISTING_BASE = BASE_URL + "/en/page/announcement_and_invitation_of_an_open_tender"
# OUTDIR = "armenia_scrapped_data"
# os.makedirs(OUTDIR, exist_ok=True)

# def setup_driver():
#     options = Options()
#     # options.add_argument("--headless")  # Uncomment for headless mode
#     service = Service(GeckoDriverManager().install())
#     return webdriver.Firefox(service=service, options=options)

# # ✅ Translation helper
# def translate_text(text):
#     if not text or pd.isna(text):
#         return text
#     try:
#         return GoogleTranslator(source='auto', target='en').translate(text)
#     except Exception as e:
#         print(f"Translation error: {e} | Text: {text}")
#         return text

# def extract_tender_details(driver, doc_url):
#     cft_id, cpv_code, estimated_value = "", "", ""
#     try:
#         driver.get(doc_url)

#         # Disable download JS
#         driver.execute_script("""
#             if (typeof downloadForAnonymousUser === 'function') {
#                 downloadForAnonymousUser = function() { console.log('Blocked downloadForAnonymousUser'); };
#             }
#         """)

#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "ShowCFTInfo"))
#         ).click()

#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "MoreCFTInfo"))
#         )

#         rows = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dt")
#         values = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dd")
#         for dt, dd in zip(rows, values):
#             label = dt.text.strip().lower()
#             value = dd.text.strip()
#             if "cft id" in label:
#                 cft_id = value
#             elif "cpv codes" in label:
#                 cpv_code = translate_text(value)  # ✅ translate
#             elif "estimated value" in label:
#                 estimated_value = translate_text(value)  # ✅ translate
#     except Exception as e:
#         print(f"⚠️ Error extracting details from {doc_url}: {e}")
#     return cft_id, cpv_code, estimated_value

# def parse_datetime(dt_str: str) -> str:
#     return dt_str.rstrip('-').strip()

# def fetch_open_tenders(page: int, today: date, driver):
#     page_url = f"{LISTING_BASE}/{page}"
#     resp = requests.get(page_url)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, 'html.parser')

#     rows = []
#     for t in soup.find_all('div', class_='tender'):
#         title_tag = t.find('div', class_='tender_title').find('p', class_='cont_text')
#         a_text = title_tag.get_text(strip=True) if title_tag else ""
#         a_text = translate_text(a_text)  # ✅ translate
#         doc_link_tag = title_tag.find('a', href=True) if title_tag else None
#         doc_link = doc_link_tag['href'] if doc_link_tag else ""
#         full_doc_link = doc_link if "http" in doc_link else BASE_URL + doc_link

#         published = ""
#         deadline = ""
#         p = t.find('p', class_='tender_time')
#         if p:
#             txt = p.get_text(strip=True).strip('()')
#             parts = txt.split('to by')
#             if len(parts) == 2:
#                 published = parse_datetime(parts[0].replace("Published", "").strip())
#                 deadline_s = parts[1].replace("time including", "").strip()
#                 deadline = deadline_s
#                 try:
#                     dead_dt = datetime.datetime.strptime(deadline_s, "%Y-%m-%d %H:%M:%S").date()
#                     if dead_dt < today:
#                         continue
#                 except:
#                     pass

#         if full_doc_link.lower().endswith(('.zip', '.rar')):
#             print(f"⏭️ Skipping link (zip/rar): {full_doc_link}")
#             cft_id, cpv_code, estimated_value = "", "", ""
#         else:
#             cft_id, cpv_code, estimated_value = extract_tender_details(driver, full_doc_link)

#         rows.append({
#             "tender_id": cft_id,
#             "tender_name": a_text,
#             "start_datetime": published,
#             "end_datetime": deadline,
#             "cpv_code": cpv_code,
#             "estimated_value": estimated_value,
#             "document_link": full_doc_link,
#             "country": "Armenia",
#             "website_link": MAIN_URL
#         })
#     return rows

# def main():
#     start_pg = int(input("Enter start page: "))
#     end_pg = int(input("Enter end page: "))
#     today = date.today()

#     driver = setup_driver()
#     try:
#         for pg in range(start_pg, end_pg + 1):
#             print(f"🔄 Processing page {pg}...")
#             data = fetch_open_tenders(pg, today, driver)
#             df = pd.DataFrame(data)
#             df = df.reindex(columns=[
#                 "tender_id",
#                 "tender_name",
#                 "start_datetime",
#                 "end_datetime",
#                 "cpv_code",
#                 "estimated_value",
#                 "document_link",
#                 "country",
#                 "website_link"
#             ])
#             out = os.path.join(OUTDIR, f"page_{pg}_open_tenders.xlsx")
#             df.to_excel(out, index=False)
#             print(f"✅ Page {pg}: {len(df)} active tenders saved to {out}")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()



# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# import datetime
# from datetime import date
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from deep_translator import GoogleTranslator

# BASE_URL = "https://gnumner.minfin.am"
# MAIN_URL = BASE_URL + "/en/page/announcement_and_invitation_of_an_open_tender/1"
# LISTING_BASE = BASE_URL + "/en/page/announcement_and_invitation_of_an_open_tender"
# OUTDIR = "armenia_scrapped_data"
# os.makedirs(OUTDIR, exist_ok=True)

# def setup_driver():
#     options = Options()
#     # options.add_argument("--headless")  # Uncomment for headless mode
#     service = Service(GeckoDriverManager().install())
#     return webdriver.Firefox(service=service, options=options)

# # ✅ Translation helper
# def translate_text(text):
#     if not text or pd.isna(text):
#         return text
#     try:
#         return GoogleTranslator(source='auto', target='en').translate(text)
#     except Exception as e:
#         print(f"Translation error: {e} | Text: {text}")
#         return text

# def extract_tender_details(driver, doc_url):
#     cft_id, cpv_code, estimated_value = "", "", ""
#     try:
#         driver.get(doc_url)

#         # Disable download JS
#         driver.execute_script("""
#             if (typeof downloadForAnonymousUser === 'function') {
#                 downloadForAnonymousUser = function() { console.log('Blocked downloadForAnonymousUser'); };
#             }
#         """)

#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "ShowCFTInfo"))
#         ).click()

#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "MoreCFTInfo"))
#         )

#         rows = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dt")
#         values = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dd")
#         for dt, dd in zip(rows, values):
#             label = dt.text.strip().lower()
#             value = dd.text.strip()
#             if "cft id" in label:
#                 cft_id = translate_text(value)  # ✅ translate CFT ID
#             elif "cpv codes" in label:
#                 cpv_code = translate_text(value)
#             elif "estimated value" in label:
#                 estimated_value = translate_text(value)
#     except Exception as e:
#         print(f"⚠️ Error extracting details from {doc_url}: {e}")
#     return cft_id, cpv_code, estimated_value

# def parse_datetime(dt_str: str) -> str:
#     return dt_str.rstrip('-').strip()

# def fetch_open_tenders(page: int, today: date, driver):
#     page_url = f"{LISTING_BASE}/{page}"
#     resp = requests.get(page_url)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, 'html.parser')

#     rows = []
#     for t in soup.find_all('div', class_='tender'):
#         title_tag = t.find('div', class_='tender_title').find('p', class_='cont_text')
#         a_text = title_tag.get_text(strip=True) if title_tag else ""
#         a_text = translate_text(a_text)  # ✅ translate name
#         doc_link_tag = title_tag.find('a', href=True) if title_tag else None
#         doc_link = doc_link_tag['href'] if doc_link_tag else ""
#         full_doc_link = doc_link if "http" in doc_link else BASE_URL + doc_link

#         published = ""
#         deadline = ""
#         p = t.find('p', class_='tender_time')
#         if p:
#             txt = p.get_text(strip=True).strip('()')
#             parts = txt.split('to by')
#             if len(parts) == 2:
#                 published = parse_datetime(parts[0].replace("Published", "").strip())
#                 deadline_s = parts[1].replace("time including", "").strip()
#                 deadline = deadline_s
#                 try:
#                     dead_dt = datetime.datetime.strptime(deadline_s, "%Y-%m-%d %H:%M:%S").date()
#                     if dead_dt < today:
#                         continue
#                 except:
#                     pass

#         if full_doc_link.lower().endswith(('.zip', '.rar')):
#             print(f"⏭️ Skipping link (zip/rar): {full_doc_link}")
#             cft_id, cpv_code, estimated_value = "", "", ""
#         else:
#             cft_id, cpv_code, estimated_value = extract_tender_details(driver, full_doc_link)

#         rows.append({
#             "tender_id": cft_id,
#             "tender_name": a_text,
#             "start_datetime": published,
#             "end_datetime": deadline,
#             "cpv_code": cpv_code,
#             "estimated_value": estimated_value,
#             "document_link": full_doc_link,
#             "country": "Armenia",
#             "website_link": MAIN_URL
#         })
#     return rows

# def main():
#     start_pg = int(input("Enter start page: "))
#     end_pg = int(input("Enter end page: "))
#     today = date.today()

#     driver = setup_driver()
#     try:
#         for pg in range(start_pg, end_pg + 1):
#             print(f"🔄 Processing page {pg}...")
#             data = fetch_open_tenders(pg, today, driver)
#             df = pd.DataFrame(data)
#             df = df.reindex(columns=[
#                 "tender_id",
#                 "tender_name",
#                 "start_datetime",
#                 "end_datetime",
#                 "cpv_code",
#                 "estimated_value",
#                 "document_link",
#                 "country",
#                 "website_link"
#             ])
#             out = os.path.join(OUTDIR, f"page_{pg}_open_tenders.xlsx")
#             df.to_excel(out, index=False)
#             print(f"✅ Page {pg}: {len(df)} active tenders saved to {out}")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()


import os
import time
import pandas as pd
import argparse
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup

# ---------------- Argument Parsing ----------------
parser = argparse.ArgumentParser(description="Scrapes tenders from Armenia website and exports to Excel.")
parser.add_argument("--starting_page", type=int, required=True, help="Page number to start scraping from.")
parser.add_argument("--run_id", type=str, required=True, help="Unique run identifier for the output folder.")
args = parser.parse_args()

# ---------------- Configuration ----------------
BASE_URL = "https://gnumner.minfin.am"
COUNTRY = 'Armenia'
WEBSITE_LINK = BASE_URL + "/en/page/announcement_and_invitation_of_an_open_tender/1"
starting_page = args.starting_page
run_id = args.run_id
today = date.today()

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs", COUNTRY, run_id)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"Created output folder: {OUTPUT_FOLDER}")

# ---------------- WebDriver Setup ----------------
print("Setting up Edge WebDriver...")
options = EdgeOptions()
# options.add_argument("--headless")  # Uncomment for headless mode
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)
driver.maximize_window()
print("WebDriver setup complete.")

# ---------------- Helper Functions ----------------
def translate_text(text):
    """Translates text to English using GoogleTranslator."""
    if not text or pd.isna(text):
        return text
    try:
        # Adding a small delay to avoid overwhelming the translation service
        time.sleep(0.5)
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e} | Original Text: {text}")
        return text

def extract_tender_details(doc_url):
    """Navigates to a tender detail page and extracts additional information."""
    cft_id, cpv_code, estimated_value = "", "", ""
    try:
        print(f"  -> Extracting details from: {doc_url}")
        driver.get(doc_url)

        # Click the button to show tender info
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ShowCFTInfo"))
        ).click()

        # Wait for the details container to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MoreCFTInfo"))
        )

        # Extract details from the definition list
        rows = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dt")
        values = driver.find_elements(By.CSS_SELECTOR, "#MoreCFTInfo dl.Grid dd")
        
        details = {}
        for dt, dd in zip(rows, values):
            label = dt.text.strip().lower()
            value = dd.text.strip()
            details[label] = value

        cft_id = translate_text(details.get("cft id", ""))
        cpv_code = translate_text(details.get("cpv codes", ""))
        estimated_value = translate_text(details.get("estimated value", ""))

    except (TimeoutException, NoSuchElementException) as e:
        print(f"  -> ⚠️ Could not extract details from {doc_url}: {e}")
    except Exception as e:
        print(f"  -> ⚠️ An unexpected error occurred while extracting details from {doc_url}: {e}")
        
    return cft_id, cpv_code, estimated_value

def parse_datetime_str(dt_str: str) -> str:
    """Helper to clean up datetime strings."""
    return dt_str.rstrip('-').strip()

def extract_tenders_from_page(page: int):
    """Extracts all tender data from a single listing page."""
    page_url = f"{BASE_URL}/en/page/announcement_and_invitation_of_an_open_tender/{page}"
    print(f"Requesting page: {page_url}")
    
    try:
        resp = requests.get(page_url, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {page}: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    tender_elements = soup.find_all('div', class_='tender')
    
    if not tender_elements:
        print("No tenders found on this page. This might be the last page.")
        return []

    tenders = []
    for t in tender_elements:
        title_tag = t.find('div', class_='tender_title').find('p', class_='cont_text')
        
        if not title_tag:
            continue

        tender_name = translate_text(title_tag.get_text(strip=True))
        doc_link_tag = title_tag.find('a', href=True)
        doc_link = doc_link_tag['href'] if doc_link_tag else ""
        full_doc_link = doc_link if "http" in doc_link else BASE_URL + doc_link

        published, deadline = "", ""
        time_tag = t.find('p', class_='tender_time')
        if time_tag:
            txt = time_tag.get_text(strip=True).strip('()')
            parts = txt.split('to by')
            if len(parts) == 2:
                published = parse_datetime_str(parts[0].replace("Published", "").strip())
                deadline_str = parts[1].replace("time including", "").strip()
                deadline = deadline_str
                try:
                    # Check if the tender is expired
                    deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S").date()
                    if deadline_dt < today:
                        print(f"  -> Skipping expired tender: {tender_name}")
                        continue
                except ValueError:
                    print(f"  -> Could not parse deadline: {deadline_str}")
                    pass
        
        # Skip downloadable files and go to detail pages for info
        if full_doc_link.lower().endswith(('.zip', '.rar', '.doc', '.docx', '.pdf')):
            print(f"  -> Skipping link (downloadable file): {full_doc_link}")
            cft_id, cpv_code, estimated_value = "", "", ""
        else:
            cft_id, cpv_code, estimated_value = extract_tender_details(full_doc_link)

        tenders.append({
            "tender_id": cft_id,
            "tender_name": tender_name,
            "start_datetime": published,
            "end_datetime": deadline,
            "cpv_code": cpv_code,
            "estimated_value": estimated_value,
            "document_link": full_doc_link,
            "country": COUNTRY,
            "website_link": WEBSITE_LINK
        })
    return tenders

# ---------------- Main Scraping Logic ----------------
current_page = starting_page
while True:
    print(f"\n--- Processing Page {current_page} ---")
    
    tenders_data = extract_tenders_from_page(current_page)

    if not tenders_data:
        print(f"No more tenders found at page {current_page}. Stopping.")
        break

    df = pd.DataFrame(tenders_data)
    df = df.reindex(columns=[
        "tender_id", "tender_name", "start_datetime", "end_datetime",
        "cpv_code", "estimated_value", "document_link", "country", "website_link"
    ])
    
    file_name = f'tenders_page_{current_page}.xlsx'
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    df.to_excel(output_file, index=False)
    print(f"✅ Saved: {len(df)} tenders to {output_file}")

    current_page += 1
    time.sleep(2)  # A polite delay between processing pages

driver.quit()
print("\nScraping completed.")



