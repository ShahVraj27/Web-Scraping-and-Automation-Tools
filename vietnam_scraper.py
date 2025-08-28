# import os
# import time
# import pandas as pd
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from deep_translator import GoogleTranslator

# # == Translator helper ==
# def translate_text(text):
#     """Translate text to English using GoogleTranslator."""
#     if not text or pd.isna(text):
#         return text
#     try:
#         return GoogleTranslator(source='auto', target='en').translate(text)
#     except Exception as e:
#         print(f"Translation error: {e} | Text: {text}")
#         return text

# # == Setup paths and browser options ==
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "vietnam_scrapped_data")
# os.makedirs(DATA_DIR, exist_ok=True)

# geckodriver_path = os.path.join(BASE_DIR, "geckodriver")  # adjust path as needed
# options = Options()
# # options.add_argument("-headless")  # uncomment for headless mode
# driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)
# wait = WebDriverWait(driver, 20)

# # == Open site and auto-select filters ==
# driver.get("https://muasamcong.mpi.gov.vn/en/web/guest/contractor-selection?render=search")
# wait.until(EC.element_to_be_clickable((By.ID, "is_not_publish_tbmt"))).click()

# # Click the "All" checkbox
# all_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "all")))
# if not all_checkbox.is_selected():
#     all_checkbox.click()

# # Click Search
# driver.find_element(By.XPATH, "//button[contains(., 'Search')]").click()

# # == Ask for page range and navigate ==
# start = int(input("Enter start page (1): ") or "1")
# end = int(input("Enter end page: ") or str(start))
# if start > 1:
#     for _ in range(start - 1):
#         wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next"))).click()
#         time.sleep(1)

# # == Helper function to format date-time ==
# def format_datetime(time_str, date_str):
#     try:
#         dt = datetime.strptime(f"{date_str.strip()} {time_str.strip()}", "%d/%m/%Y %H:%M")
#         return dt.strftime("%d-%m-%Y  %H:%M:%S")
#     except:
#         return ""

# def format_combined_datetime(date_time_str):
#     try:
#         date_part, time_part = [x.strip() for x in date_time_str.split('-')]
#         return format_datetime(time_part, date_part)
#     except:
#         return ""

# current = start
# while current <= end:
#     print(f"\n📄 Scraping page {current} ...")
#     wait.until(EC.presence_of_all_elements_located(
#         (By.CSS_SELECTOR, "div.content__body__left__item")
#     ))
#     items = driver.find_elements(By.CSS_SELECTOR, "div.content__body__left__item")

#     rows = []
#     for idx, item in enumerate(items, start=1):
#         def safe_text(by, selector):
#             try:
#                 return item.find_element(by, selector).text.strip()
#             except:
#                 return ""

#         no_full = safe_text(By.CSS_SELECTOR, "p:nth-child(1)")
#         no = no_full.replace("Invitation-to-bid No :", "").strip()
#         name = translate_text(safe_text(By.XPATH, ".//h5[contains(@class, 'contract__name')]"))
#         proc = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Procuring Entity')]/span"))
#         emp = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Employer')]/span"))

#         raw_pub_datetime = safe_text(By.XPATH, ".//h6[contains(.,'publication date')]/span")
#         pub_date = format_combined_datetime(raw_pub_datetime)

#         category = translate_text(safe_text(By.XPATH, ".//h6[contains(text(),'Field')]/span"))
#         place = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Place')]/span"))

#         deadline = ""
#         try:
#             offer_end_time = item.find_elements(By.XPATH, ".//p[contains(text(), 'End time of online price offering')]/following-sibling::h5")
#             if len(offer_end_time) >= 2:
#                 deadline = format_datetime(offer_end_time[0].text, offer_end_time[1].text)
#             else:
#                 closing_time_elements = item.find_elements(By.XPATH, ".//p[contains(text(), 'Bid closing time')]/following-sibling::h5")
#                 if len(closing_time_elements) >= 2:
#                     deadline = format_datetime(closing_time_elements[0].text, closing_time_elements[1].text)
#         except:
#             pass

#         mode = translate_text(safe_text(By.XPATH, ".//p[contains(text(), 'Bid submission procedure')]/following-sibling::h5[1]"))

#         rows.append({
#             "Tender No": no,
#             "Name of Work/Tender": name,
#             "Category": category,
#             "Procuring Entity/Ministry or Department": proc,
#             "Employer": emp,
#             "Start Date": pub_date,
#             "CLosing Date": deadline,
#             "Location": place,
#             "Submission Mode": mode,
#             "EMD": "",
#             "Exemption for EMD": "",
#             "Country": "Vietnam",
#             "Document link": "",
#             "CPV codes": "",
#             "Website link": "https://muasamcong.mpi.gov.vn/en/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index&indexSelect=null"
#         })

#     df = pd.DataFrame(rows)
#     file_path = os.path.join(DATA_DIR, f"tenders_page_{current}.xlsx")
#     df.to_excel(file_path, index=False)
#     print(f"✅ Saved {len(rows)} rows to {file_path}")

#     current += 1
#     if current <= end:
#         try:
#             wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next"))).click()
#             time.sleep(1)
#         except:
#             print("⚠️ Could not navigate to next page. Stopping.")
#             break

# driver.quit()


import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator

# == Translator helper ==
def translate_text(text):
    """Translate text to English using GoogleTranslator."""
    if not text or pd.isna(text):
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e} | Text: {text}")
        return text

# == Setup paths and browser options ==
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "vietnam_scrapped_data")
os.makedirs(DATA_DIR, exist_ok=True)

geckodriver_path = os.path.join(BASE_DIR, "geckodriver")  # Adjust as needed
options = Options()
# options.add_argument("-headless")  # Uncomment for headless mode
driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)
wait = WebDriverWait(driver, 20)

# == Open site and auto-select filters ==
driver.get("https://muasamcong.mpi.gov.vn/en/web/guest/contractor-selection?render=search")
wait.until(EC.element_to_be_clickable((By.ID, "is_not_publish_tbmt"))).click()

# Click the "All" checkbox
all_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "all")))
if not all_checkbox.is_selected():
    all_checkbox.click()

# Click Search
driver.find_element(By.XPATH, "//button[contains(., 'Search')]").click()

# == Ask for page range and navigate ==
start = int(input("Enter start page (1): ") or "1")
end = int(input("Enter end page: ") or str(start))
if start > 1:
    for _ in range(start - 1):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next"))).click()
        time.sleep(1)

# == Helper functions for datetime ==
def format_datetime(time_str, date_str):
    try:
        dt = datetime.strptime(f"{date_str.strip()} {time_str.strip()}", "%d/%m/%Y %H:%M")
        return dt.strftime("%d-%m-%Y  %H:%M:%S")
    except:
        return ""

def format_combined_datetime(date_time_str):
    try:
        date_part, time_part = [x.strip() for x in date_time_str.split('-')]
        return format_datetime(time_part, date_part)
    except:
        return ""

# == Main scraping loop ==
current = start
while current <= end:
    print(f"\n📄 Scraping page {current} ...")
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.content__body__left__item")))
    items = driver.find_elements(By.CSS_SELECTOR, "div.content__body__left__item")

    rows = []
    for idx, item in enumerate(items, start=1):
        def safe_text(by, selector):
            try:
                return item.find_element(by, selector).text.strip()
            except:
                return ""

        no_full = safe_text(By.CSS_SELECTOR, "p:nth-child(1)")
        no = no_full.replace("Invitation-to-bid No :", "").strip()

        # 🔗 Extract name and document link
        try:
            name_element = item.find_element(By.XPATH, ".//a[contains(@href, 'guest/contractor-select')]")
            name = translate_text(name_element.text.strip())
            doc_link = name_element.get_attribute("href")
        except:
            name = ""
            doc_link = ""

        proc = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Procuring Entity')]/span"))
        emp = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Employer')]/span"))

        raw_pub_datetime = safe_text(By.XPATH, ".//h6[contains(.,'publication date')]/span")
        pub_date = format_combined_datetime(raw_pub_datetime)

        category = translate_text(safe_text(By.XPATH, ".//h6[contains(text(),'Field')]/span"))
        place = translate_text(safe_text(By.XPATH, ".//h6[contains(.,'Place')]/span"))

        deadline = ""
        try:
            offer_end_time = item.find_elements(By.XPATH, ".//p[contains(text(), 'End time of online price offering')]/following-sibling::h5")
            if len(offer_end_time) >= 2:
                deadline = format_datetime(offer_end_time[0].text, offer_end_time[1].text)
            else:
                closing_time_elements = item.find_elements(By.XPATH, ".//p[contains(text(), 'Bid closing time')]/following-sibling::h5")
                if len(closing_time_elements) >= 2:
                    deadline = format_datetime(closing_time_elements[0].text, closing_time_elements[1].text)
        except:
            pass

        mode = translate_text(safe_text(By.XPATH, ".//p[contains(text(), 'Bid submission procedure')]/following-sibling::h5[1]"))

        rows.append({
            "Tender No": no,
            "Name of Work/Tender": name,
            "Category": category,
            "Procuring Entity/Ministry or Department": proc,
            "Employer": emp,
            "Start Date": pub_date,
            "CLosing Date": deadline,
            "Location": place,
            "Submission Mode": mode,
            "EMD": "",
            "Exemption for EMD": "",
            "Country": "Vietnam",
            "Document link": doc_link,
            "CPV codes": "",
            "Website link": "https://muasamcong.mpi.gov.vn/en/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index&indexSelect=null"
        })

    df = pd.DataFrame(rows)
    file_path = os.path.join(DATA_DIR, f"tenders_page_{current}.xlsx")
    df.to_excel(file_path, index=False)
    print(f"✅ Saved {len(rows)} rows to {file_path}")

    current += 1
    if current <= end:
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next"))).click()
            time.sleep(1)
        except:
            print("⚠️ Could not navigate to next page. Stopping.")
            break

driver.quit()
