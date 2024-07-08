from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re



driver = webdriver.Chrome()

driver.get("https://www.southtechhosting.com/SanDiegoCounty/CampaignDocsWebRetrieval/Search/SearchByFilerName.aspx")

element = driver.find_element(By.ID, "ctl00_DefaultContent_ASPxRoundPanel1_txtFilerName_I") 
element.send_keys("teacher") 

element = driver.find_element(By.ID, "ctl00_DefaultContent_ASPxRoundPanel1_btnFindFilers")
element.click()
 
WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']")))

css_elements = driver.find_elements(By.CSS_SELECTOR, "img.dx-vam[src*='../Images/view.png']")

img_id1 = "ctl00_GridContent_gridFilers_DXCBtn"
img_id2 = "Img"

for i in range(len(css_elements)):
    img_id = str(img_id1 + str(i) + img_id2)
    WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((By.ID, img_id))).click()
    WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((By.ID, "ctl00_DefaultContent_lblFilerNames")))
    filer = driver.find_element(By.ID, "ctl00_DefaultContent_lblFilerNames")
    print(filer.text)
    
    # detect for downloadables
    try: 
        
        
        WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.dx-vam[src*='../Images/excell.jpg']")))  
        table = driver.find_element(By.ID, "ctl00_DefaultContent_gridFilingForms_DXMainTable")
        tr_list = table.find_elements(By.TAG_NAME, "tr")
        # download
        for i in tr_list:
            if '496' in str(i.text):
                excel = i.find_element(By.CSS_SELECTOR, "img.dx-vam[src*='../Images/excell.jpg']").click()
                print(i.text)
        
        # go back and repeat
        time.sleep(10)
        driver.back()
    except:
        continue
    

    
# for i in element:
#     i.click()
#     time.sleep(10)
#     driver.back()
#     time.sleep(10)
    


