from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

study_ids = ['NCT01714739','NCT05844007','NCT05780424']
# URL of the clinical trial page
URL = 'https://www.clinicaltrials.gov/study/REPLACE_NCTID?tab=table#recruitment-information'
RECRUITMENT_TAB=4

# Configure Chrome options for headless browsing
options = Options()
options.headless = True

# Start Chrome WebDriver
for nct_id in study_ids:
    study_url = URL.replace('REPLACE_NCTID',nct_id)
    with webdriver.Chrome(options=options) as driver:
        # Load the page
        driver.get(study_url)

        # Wait until the recruitment information header is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'recruitment-information')))

        # Get the page source
        page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    recruitment_info_section = soup.find_all('div', class_='table', attrs={'_ngcontent-ng-c1086300613': ''})[RECRUITMENT_TAB]


    # Get the data for indiviudal study
    dict = {}
    get_next_section = False
    name = ""
    for section in recruitment_info_section:
        # Get actual/Estimated enrollment value for dict
        if get_next_section:
            dict[name] = section.text
        get_next_section = False
        # Get actual/Estimated enrollment key for dict
        if 'Enrollment' in section.text :
            # print("Enrollment: ",section.text)
            dict[section.text] = -1
            name = section.text
            get_next_section = True

    print(dict)
    time.sleep(1)

