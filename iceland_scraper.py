# import os
# import time
# from datetime import datetime
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from deep_translator import GoogleTranslator

# def translate_text(text):
#     if not text or pd.isna(text):
#         return text
#     try:
#         return GoogleTranslator(source='auto', target='en').translate(text)
#     except Exception as e:
#         print(f"Translation error: {e} | Text: {text}")
#         return text

# def parse_deadline(text):
#     try:
#         return datetime.strptime(text, "%d.%m.%Y kl. %H:%M")
#     except:
#         return None

# # Setup
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "iceland_scrapped_data")
# os.makedirs(DATA_DIR, exist_ok=True)
# geckodriver_path = os.path.join(BASE_DIR, "geckodriver")

# options = Options()
# # options.add_argument("--headless")
# driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)

# try:
#     max_items = int(input("How many tenders to scrape? "))
# except ValueError:
#     print("Invalid number. Exiting.")
#     driver.quit()
#     exit()

# try:
#     driver.get("https://www.utbodsvefur.is/")
#     WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
#     rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
# except Exception as e:
#     print(f"❌ Error loading website: {e}")
#     driver.quit()
#     exit()

# count = 0
# batch = 1
# batch_data = []

# for row in rows:
#     if count >= max_items:
#         break

#     try:
#         cols = row.find_elements(By.TAG_NAME, "td")
#         cells = [c.text.strip() for c in cols] + [""] * (5 - len(cols))
#         num = cells[0]

#         try:
#             link_elem = cols[1].find_element(By.TAG_NAME, "a")
#             title = link_elem.text.strip()
#             doc_link = link_elem.get_attribute("href")
#         except:
#             title = cells[1]
#             doc_link = ""

#         agency, kind, deadline = cells[2:5]

#         dt = parse_deadline(deadline)
#         if dt and dt <= datetime.now():
#             continue

#         title_en = translate_text(title)
#         agency_en = translate_text(agency)
#         kind_en = translate_text(kind)

#         # Default blank values
#         publishing_date = ""
#         start_date = ""

#         # ✅ Visit detail page to extract publishing/start dates
#         if doc_link:
#             try:
#                 driver.execute_script("window.open('');")
#                 driver.switch_to.window(driver.window_handles[1])
#                 driver.get(doc_link)
#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

#                 rows_detail = driver.find_elements(By.CSS_SELECTOR, "table tr")

#                 for tr in rows_detail:
#                     try:
#                         ths = tr.find_elements(By.TAG_NAME, "td")
#                         if len(ths) >= 2:
#                             label = ths[0].text.strip()
#                             value = ths[1].text.strip()
#                             if "Útboðsgögn afhent" in label:
#                                 publishing_date = value
#                             elif "Opnun tilboða" in label:
#                                 start_date = value
#                     except:
#                         continue

#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#             except Exception as e:
#                 print(f"⚠️ Could not process detail page: {e}")
#                 if len(driver.window_handles) > 1:
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])

#         # Save row
#         batch_data.append({
#             "Tender No": num,
#             "Name of Work/Tender": title_en,
#             "Procuring Entity/Ministry or Department": agency_en,
#             "Category": kind_en,
#             "Start Date": start_date,
#             "Closing Date": deadline,
#             "Publishing Date": publishing_date,
#             "Employer": agency_en,
#             "Location": "",
#             "Submission Mode": "",
#             "EMD": "",
#             "Exemption for EMD": "",
#             "Country": "Iceland",
#             "Document link": doc_link,
#             "CPV codes": "",
#             "Website link": "https://www.utbodsvefur.is/"
#         })

#         count += 1

#         if count % 20 == 0 or count == max_items:
#             df = pd.DataFrame(batch_data)
#             file_path = os.path.join(DATA_DIR, f"tenders_batch_{batch}.xlsx")
#             df.to_excel(file_path, index=False)
#             print(f"✅ Saved {len(batch_data)} tenders to {file_path}")
#             batch += 1
#             batch_data = []

#     except Exception as e:
#         print(f"⚠️ Skipping row due to error: {e}")
#         continue

# driver.quit()
# print(f"🎉 Done! Total tenders saved: {count}")



import os
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator

def translate_text(text):
    if not text or pd.isna(text):
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e} | Text: {text}")
        return text

def parse_datetime(text):
    try:
        dt = datetime.strptime(text, "%d.%m.%Y kl. %H:%M")
        return dt.strftime("%d-%m-%Y  %H:%M:%S")
    except:
        return ""

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "iceland_scrapped_data")
os.makedirs(DATA_DIR, exist_ok=True)
geckodriver_path = os.path.join(BASE_DIR, "geckodriver")

options = Options()
# options.add_argument("--headless")
driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)

try:
    max_items = int(input("How many tenders to scrape? "))
except ValueError:
    print("Invalid number. Exiting.")
    driver.quit()
    exit()

try:
    driver.get("https://www.utbodsvefur.is/")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
except Exception as e:
    print(f"❌ Error loading website: {e}")
    driver.quit()
    exit()

count = 0
batch = 1
batch_data = []

for row in rows:
    if count >= max_items:
        break

    try:
        cols = row.find_elements(By.TAG_NAME, "td")
        cells = [c.text.strip() for c in cols] + [""] * (5 - len(cols))
        num = cells[0]

        try:
            link_elem = cols[1].find_element(By.TAG_NAME, "a")
            title = link_elem.text.strip()
            doc_link = link_elem.get_attribute("href")
        except:
            title = cells[1]
            doc_link = ""

        agency, kind, deadline_raw = cells[2:5]
        deadline = parse_datetime(deadline_raw)

        if not deadline:
            continue

        title_en = translate_text(title)
        agency_en = translate_text(agency)
        kind_en = translate_text(kind)

        tender_pub = ""
        bid_start = ""

        # Visit detail page
        if doc_link:
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(doc_link)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

                rows_detail = driver.find_elements(By.CSS_SELECTOR, "table tr")

                for tr in rows_detail:
                    try:
                        ths = tr.find_elements(By.TAG_NAME, "td")
                        if len(ths) >= 2:
                            label = ths[0].text.strip()
                            value = ths[1].text.strip()
                            if "Útboðsgögn afhent" in label:
                                tender_pub = parse_datetime(value)
                            elif "Opnun tilboða" in label:
                                bid_start = parse_datetime(value)
                    except:
                        continue

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print(f"⚠️ Could not process detail page: {e}")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        # Append to data
        batch_data.append({
            "Tender No": num,
            "Name of Work/Tender": title_en,
            "Procuring Entity/Ministry or Department": agency_en,
            "Category": kind_en,
            "Bid Starting Date": bid_start,
            "Bid Closing Date": deadline,
            "Tender Documents Publishing Date": tender_pub,
            "Employer": agency_en,
            "Location": "",
            "Submission Mode": "",
            "EMD": "",
            "Exemption for EMD": "",
            "Country": "Iceland",
            "Document link": doc_link,
            "Website link": "https://www.utbodsvefur.is/"
        })

        count += 1

        if count % 20 == 0 or count == max_items:
            df = pd.DataFrame(batch_data)
            file_path = os.path.join(DATA_DIR, f"tenders_batch_{batch}.xlsx")
            df.to_excel(file_path, index=False)
            print(f"✅ Saved {len(batch_data)} tenders to {file_path}")
            batch += 1
            batch_data = []

    except Exception as e:
        print(f"⚠️ Skipping row due to error: {e}")
        continue

driver.quit()
print(f"🎉 Done! Total tenders saved: {count}")
