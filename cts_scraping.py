from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

study_ids = [
'NCT01714739','NCT05844007','NCT05780424','NCT03243422','NCT05769322',
'NCT05831722','NCT06190522','NCT05415722','NCT04525222','NCT05428722',
'NCT04540822','NCT05272748','NCT06003439','NCT00341939','NCT06264401',
'NCT03452930','NCT01556230','NCT04863040','NCT06150274','NCT05174065',
'NCT04605822','NCT05140330','NCT06125730','NCT06407622','NCT03946839',
'NCT05739539','NCT04373265','NCT05690165','NCT05395065','NCT06054074',
'NCT01916122','NCT06106230','NCT06106022','NCT03412565','NCT04317066',
'NCT06278766','NCT05129566','NCT05996874','NCT03005782','NCT04456920',
'NCT05328622','NCT05201339','NCT05187039','NCT02366039','NCT03842722',
'NCT06325839','NCT06237530','NCT04455230','NCT03987425','NCT05063422'
]
# study_ids = ['NCT05780424','NCT05831722','NCT06190522','NCT00341939','NCT06125730','NCT06407622','NCT03842722','NCT06325839','NCT06237530']
if len(study_ids) != len(set(study_ids)):
    print("Duplicates")
# study_ids = ['NCT05831722']
# URL of the clinical trial page
URL = 'https://www.clinicaltrials.gov/study/REPLACE_NCTID?tab=table#recruitment-information'
RECRUITMENT_TAB=4

# Configure Chrome options for headless browsing
options = Options()
options.headless = True
# Using Dataframe to write to xls
df = pd.DataFrame(columns=('study_id', 'ActualEnrollment', 'OriginalEnrollment'))
# Start Chrome WebDriver
for nct_id in study_ids:
    # print("nct_id:: ",nct_id)
    study_url = URL.replace('REPLACE_NCTID',nct_id)
    with webdriver.Chrome(options=options) as driver:
        # Load the page
        driver.get(study_url)

        # Wait until the recruitment information header is present
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'recruitment-information')))

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
            # print("section.text:: ",section.text)
        get_next_section = False
        # Get actual/Estimated enrollment key for dict
        if 'Enrollment' in section.text :
            # print("Enrollment: ",section.text)
            dict[section.text] = -1
            name = section.text
            get_next_section = True

    # print(dict)
    actual_val = -1
    estimated_val = -1
    if len(dict) == 2:
        for key, value in dict.items():
            # print(key, value)
            if 'Original' in key:
                estimated_val = value
            elif 'Actual' in key:
                actual_val = value

        print('study_id: ', nct_id," Actual: ",actual_val, " Estimated: ",estimated_val)
        if actual_val != -1 and estimated_val != -1:
            # print(actual_val, estimated_val)
            new_row = {'study_id':nct_id,'ActualEnrollment':actual_val,'OriginalEnrollment':estimated_val}
            df.loc[len(df)] = new_row
        else:
            print("**"*10)
            print("Error:: Data not entered for id: ",nct_id)
            print("Values in dict: ",dict)
    time.sleep(1)
# Print and write to xls
# print(df)
df.to_excel("output.xlsx")
