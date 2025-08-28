# import os
# import time
# import datetime
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from deep_translator import GoogleTranslator
# from datetime import datetime

# # Get base directory of the Python file
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def setup_driver():
#     """Set up and return a configured Firefox WebDriver."""
#     firefox_options = Options()
#     firefox_options.add_argument("--start-maximized")
#     firefox_options.add_argument("--disable-notifications")
#     firefox_options.add_argument("--disable-popup-blocking")
    
#     service = Service(GeckoDriverManager().install())
#     driver = webdriver.Firefox(service=service, options=firefox_options)
#     return driver

# def translate_text(text):
#     """Translate text from Russian to English."""
#     try:
#         return GoogleTranslator(source='ru', target='en').translate(text)
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text

# def scrape_page(driver, page_num):
#     """Scrape a single page of auctions."""
#     try:
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, "//table//tr[2]"))
#         )
#         auctions_data = []
#         rows = driver.find_elements(By.XPATH, "//table//tr[position()>1]")
#         for row in rows:
#             try:
#                 cells = row.find_elements(By.TAG_NAME, "td")

#                 # ✅ Skip rows with too few cells or empty Tender No
#                 if len(cells) < 10 or not cells[0].text.strip():
#                     continue

#                 auction_info = {}
#                 auction_info["Tender No"] = cells[0].text.strip()
#                 auction_info["Name of Work"] = cells[1].text.strip()
#                 auction_info["Category"] = cells[2].text.strip()
#                 auction_info["Estimated Cost (Belarusian Ruble)"] = cells[4].text.strip()
#                 auction_info["Customer/organizer"] = cells[5].text.strip()
#                 auction_info["Ministry and Department"] = cells[6].text.strip()
#                 auction_info["Date of publication"] = cells[3].text.strip()
#                 auction_info["Closing Date/Deadline"] = cells[7].text.strip()
#                 auction_info["Condition"] = cells[9].text.strip()
#                 # Additional fields
#                 auction_info["EMD"] = ""
#                 auction_info["Exemption for EMD"] = ""
#                 auction_info["Country"] = "Belarus"
#                 auction_info["Apply mode"] = ""
#                 auction_info["Website link"] = "https://zakupki.butb.by/auctions/reestrauctions.html"
#                 auction_info["Document link"] = ""
#                 auction_info["CPV codes"] = ""
#                 auctions_data.append(auction_info)

#                 print(auction_info)
#             except Exception as e:
#                 print(f"Error processing auction row: {e}")
#                 continue
#         return auctions_data
#     except Exception as e:
#         print(f"Error scraping page {page_num}: {e}")
#         return None

# def main():
#     if not os.path.exists("belarus_scrapped_data"):
#         os.makedirs("belarus_scrapped_data")

#     start_page = int(input("Enter the starting page number: "))
#     end_page = int(input("Enter the ending page number: "))

#     driver = setup_driver()

#     try:
#         url = "https://zakupki.butb.by/auctions/reestrauctions.html#?page=1"
#         driver.get(url)
#         time.sleep(2)

#         for page_num in range(start_page, end_page + 1):
#             if page_num != 1:
#                 page_btn_xpath = f"//a[text()='{page_num}']"
#                 try:
#                     page_btn = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, page_btn_xpath))
#                     )
#                     page_btn.click()
#                     time.sleep(2)
#                 except Exception as e:
#                     print(f"Error navigating to page {page_num}: {e}")
#                     break

#             print(f"\nScraping page {page_num}...")
#             auctions_data = scrape_page(driver, page_num)
#             if auctions_data:
#                 columns = [
#                     "Tender No", "Name of Work", "Category", "Estimated Cost (Belarusian Ruble)",
#                     "Customer/organizer", "Ministry and Department", "Date of publication",
#                     "Closing Date/Deadline", "Condition", "EMD", "Exemption for EMD", "Country",
#                     "Apply mode", "Website link", "Document link", "CPV codes"
#                 ]
#                 df = pd.DataFrame(auctions_data, columns=columns)
#                 excel_file = f"belarus_scrapped_data/tenders_Page_{page_num}.xlsx"
#                 df.to_excel(excel_file, index=False)
#                 print(f"✅ Data saved to {excel_file}")
#             else:   
#                 print(f"❌ No data found on page {page_num}")

#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         driver.quit()
#         print("\nScraping completed!")

# if __name__ == "__main__":
#     main()



import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from deep_translator import GoogleTranslator
from datetime import datetime

# Get base directory of the Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_driver():
    """Set up and return a configured Firefox WebDriver."""
    firefox_options = Options()
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument("--disable-notifications")
    firefox_options.add_argument("--disable-popup-blocking")
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def translate_text(text):
    """Translate text to English using GoogleTranslator."""
    if not text or pd.isna(text):
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e} | Text: {text}")
        return text

def scrape_page(driver, page_num):
    """Scrape a single page of auctions."""
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//table//tr[2]"))
        )
        auctions_data = []
        rows = driver.find_elements(By.XPATH, "//table//tr[position()>1]")
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")

                # ✅ Skip rows with too few cells or empty Tender No
                if len(cells) < 10 or not cells[0].text.strip():
                    continue

                auction_info = {}
                auction_info["Tender No"] = cells[0].text.strip()
                auction_info["Name of Work"] = translate_text(cells[1].text.strip())
                auction_info["Category"] = translate_text(cells[2].text.strip())
                auction_info["Estimated Cost (Belarusian Ruble)"] = cells[4].text.strip()
                auction_info["Customer/organizer"] = translate_text(cells[5].text.strip())
                auction_info["Ministry and Department"] = translate_text(cells[6].text.strip())
                auction_info["Date of publication"] = cells[3].text.strip()
                auction_info["Closing Date/Deadline"] = cells[7].text.strip()
                auction_info["Condition"] = translate_text(cells[9].text.strip())

                # Additional fields
                auction_info["EMD"] = ""
                auction_info["Exemption for EMD"] = ""
                auction_info["Country"] = "Belarus"
                auction_info["Apply mode"] = ""
                auction_info["Website link"] = "https://zakupki.butb.by/auctions/reestrauctions.html"
                auction_info["Document link"] = ""
                auction_info["CPV codes"] = ""

                auctions_data.append(auction_info)
                print(auction_info)
            except Exception as e:
                print(f"Error processing auction row: {e}")
                continue
        return auctions_data
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return None

def main():
    if not os.path.exists("belarus_scrapped_data"):
        os.makedirs("belarus_scrapped_data")

    start_page = int(input("Enter the starting page number: "))
    end_page = int(input("Enter the ending page number: "))

    driver = setup_driver()

    try:
        url = "https://zakupki.butb.by/auctions/reestrauctions.html#?page=1"
        driver.get(url)
        time.sleep(2)

        for page_num in range(start_page, end_page + 1):
            if page_num != 1:
                page_btn_xpath = f"//a[text()='{page_num}']"
                try:
                    page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, page_btn_xpath))
                    )
                    page_btn.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Error navigating to page {page_num}: {e}")
                    break

            print(f"\nScraping page {page_num}...")
            auctions_data = scrape_page(driver, page_num)
            if auctions_data:
                columns = [
                    "Tender No", "Name of Work", "Category", "Estimated Cost (Belarusian Ruble)",
                    "Customer/organizer", "Ministry and Department", "Date of publication",
                    "Closing Date/Deadline", "Condition", "EMD", "Exemption for EMD", "Country",
                    "Apply mode", "Website link", "Document link", "CPV codes"
                ]
                df = pd.DataFrame(auctions_data, columns=columns)
                excel_file = f"belarus_scrapped_data/tenders_Page_{page_num}.xlsx"
                df.to_excel(excel_file, index=False)
                print(f"✅ Data saved to {excel_file}")
            else:
                print(f"❌ No data found on page {page_num}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("\nScraping completed!")

if __name__ == "__main__":
    main()
