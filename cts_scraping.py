from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

def getStudyData():
    # study_ids = [ 'NCT00341939']
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
    ADMIN_TAB = 5

    # Configure Chrome options for headless browsing
    options = Options()
    options.headless = True
    # Using Dataframe to write to xls
    df = pd.DataFrame(columns=('study_id', 'ActualEnrollment', 'OriginalEnrollment',
                               'StudyStartDate','StudyCompletionDate','CurrentStudySponsor','OriginalStudySponsor'))
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
        all_sections = soup.find_all('div', class_='table', attrs={'_ngcontent-ng-c1086300613': ''})
        recruitment_section = all_sections[RECRUITMENT_TAB]
        admin_section = all_sections[ADMIN_TAB]


        # Get the data for indiviudal study
        dict = {}
        get_next_section = False
        name = ""
        for section in recruitment_section:
            # Get actual/Estimated enrollment value for dict
            if get_next_section:
                dict[name] = section.text
            get_next_section = False
            # Get actual/Estimated enrollment key for dict
            if 'Enrollment'  in section.text :
                dict[section.text] = -1
                name = section.text
                get_next_section = True
            elif 'Study Start Date' in section.text :
                dict[section.text] = -1
                name = section.text
                get_next_section = True
            elif 'Study Completion Date' in section.text :
                dict[section.text] = -1
                name = section.text
                get_next_section = True

        get_next_section = False
        for section in admin_section:
            # Get actual/Estimated enrollment value for dict
            if get_next_section:
                dict[name] = section.text
            get_next_section = False
            # Get actual/Estimated enrollment key for dict
            if 'Sponsor' in section.text :
                dict[section.text] = -1
                name = section.text
                get_next_section = True

        actual_val,estimated_val = -1,-1
        start_date,com_date,current_sponsor,orig_sponsor = '','','',''
        if len(dict) == 6:
            for key, value in dict.items():
                if 'Original Enrollment' in key:
                    estimated_val = value
                elif 'Enrollment (Actual)' in key:
                    actual_val = value
                elif 'Start' in key:
                    start_date = value
                elif 'Completion' in key:
                    com_date = value
                elif 'Current Study Sponsor' in key:
                    current_sponsor = value
                elif 'Original Study Sponsor' in key:
                    orig_sponsor = value

            # print('study_id: ', nct_id," Actual: ",actual_val, " Estimated: ",estimated_val)
            # print('StudyStartDate: ', start_date, " StudyCompletionDate: ", com_date, " CurrentStudySponsor: ", current_sponsor, "OriginalStudySponsor:",orig_sponsor )
            if actual_val != -1 and estimated_val != -1:
                # print(actual_val, estimated_val)
                new_row = {'study_id':nct_id,'ActualEnrollment':actual_val,'OriginalEnrollment':estimated_val,
                           'StudyStartDate':start_date, 'StudyCompletionDate':com_date, 'CurrentStudySponsor':current_sponsor,
                           'OriginalStudySponsor':orig_sponsor}
                df.loc[len(df)] = new_row
            else:
                print("**"*10)
                print("Error:: Data not entered for id: ",nct_id)
                print("Values in dict: ",dict)
        time.sleep(1)
    # Print and write to xls
    # print(df)
    df.to_excel("output.xlsx")
def calDiff():
    if os.path.exists("./output.xlsx"):
        print("File exists")
        excel_data_df = pd.read_excel("./output.xlsx", dtype=str,index_col=0)
        excel_data_df['difference'] =  excel_data_df.apply(lambda x: int(x['ActualEnrollment']) - int(x['OriginalEnrollment']) if x['OriginalEnrollment'] != 'Same as current' and str(x['ActualEnrollment']) != 'Same as current' else 0,axis=1)
        excel_data_df.style.apply(lambda x:(None,None,None,'background-color: green',None,None,None,None) if x['difference'] >0  else (None,None,None,'background-color: red',None,None,None,None), axis=1).to_excel("./new_output.xlsx")
        # print(excel_data_df)

    else:
        print("File does not exist")

if __name__ == "__main__":
    getStudyData()
    calDiff()

