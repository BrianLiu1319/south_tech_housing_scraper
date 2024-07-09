# since page 2 of teachers doesnt work and only san marcos has 496 im hard coding this

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def extract_date(text):
    date_pattern = r"\b(\d{1,2}/\d{1,2}/\d{4})\b"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def reformat_date(date_str):
    if date_str:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        # Format the date into YYYYMMDD
        return date_obj.strftime("%Y%m%d")
    return None


options = Options()
options.add_experimental_option(
    "prefs",
    {"download.default_directory": r"C:\Users\brian\Desktop\sdcta\scraper\exportspt2"},
)

s = Service()


driver = webdriver.Chrome(service=s, options=options)

driver.get(
    "https://www.southtechhosting.com/SanDiegoCounty/CampaignDocsWebRetrieval/Search/SearchByFilerName.aspx"
)

element = driver.find_element(
    By.ID, "ctl00_DefaultContent_ASPxRoundPanel1_txtFilerName_I"
)

# determine which name to search for
element.send_keys("teacher")
element = driver.find_element(
    By.ID, "ctl00_DefaultContent_ASPxRoundPanel1_btnFindFilers"
)
element.click()

# Wait until image is loaded
WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']")
    )
)


# get all possible filers
css_elements = driver.find_elements(
    By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']"
)


count = 0


next_button = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.XPATH, "//img[@src='../App_Themes/Glass/Web/pNext.png']")
    )
)

next_button.click()
time.sleep(7)

WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']")
    )
)
css_elements = driver.find_elements(
    By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']"
)

txt = "./exportspt2/dates.txt"
img_id1 = "ctl00_GridContent_gridFilers_DXCBtn"
img_id2 = "Img"

with open(txt, "a") as file:
    img_id = str(img_id1 + str(5) + img_id2)
    new_school = WebDriverWait(driver, timeout=20).until(
        EC.presence_of_element_located((By.ID, img_id))
    )
    new_school.click()

    WebDriverWait(driver, timeout=20).until(
        EC.presence_of_element_located((By.ID, "ctl00_DefaultContent_lblFilerNames"))
    )

    filer = driver.find_element(By.ID, "ctl00_DefaultContent_lblFilerNames")
    
    WebDriverWait(driver, timeout=2).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "img.dx-vam[src*='../Images/excell.jpg']")
        )
    )
    table = driver.find_element(
        By.ID, "ctl00_DefaultContent_gridFilingForms_DXMainTable"
    )
    tr_list = table.find_elements(By.TAG_NAME, "tr")
    for i in tr_list:
        if "496" in str(i.text):
            # download
            excel = i.find_element(
                By.CSS_SELECTOR, "img.dx-vam[src*='../Images/excell.jpg']"
            ).click()
            
            date = extract_date(i.text)
            date = reformat_date(date)
            filename = date + " 496-" + str(count) + ".xls"
            count += 1
            file.write(filename + "\n")
