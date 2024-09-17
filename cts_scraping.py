from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import requests
import os
import argparse
from datetime import datetime

study_ids = []
RECRUITMENT_TAB = 4
ADMIN_TAB = 5

def get_studies_data_from_cts(base_url, params, headers):
    studies = []
    while base_url:
        # Get Data
        response = requests.get(base_url, params=params, headers=headers)
        # Success
        if response.status_code == 200:
            data = response.json()
            studies.extend(data.get('studies', []))
            next_page_token = data.get('nextPageToken', None)
            if next_page_token:
                params['pageToken'] = next_page_token
            else:
                break
        else:
            print(f"Error: Unable to fetch data (status code {response.status_code})")
            print(response.text)
            return None
    return studies

def get_study_ids(sponsor, date_range_start, date_range_end):
    # Base URL for ClinicalTrials.gov API
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        # "query.spons": sponsor,   # Only for sponsor
        "filter.overallStatus": "COMPLETED",  # Get only completed studies
        # "filter.advanced": f"AREA[CompletionDate]RANGE[{date_range_start}, {date_range_end}]",
        "postFilter.overallStatus": "COMPLETED", # Get only completed studies
        "fields": "protocolSection.identificationModule.nctId"  # Configurable fields
    }

    if len(sponsor) > 0:
        params["query.spons"] = sponsor
    if len(date_range_start) == 10 and len(date_range_end) == 10:
        params["filter.advanced"] = f"AREA[CompletionDate]RANGE[{date_range_start}, {date_range_end}]"
    else:
        print(f"Error: date_range_start and date_range_end both should be passed)")
        return None

    headers = {
        "accept": "application/json"
    }

    # Get the data
    studies_data = get_studies_data_from_cts(base_url, params, headers)
    if studies_data:
        for study in studies_data:
            nct_id = study.get('protocolSection', '').get('identificationModule', '').get('nctId', '')
            if len(nct_id) > 0:
                study_ids.append(nct_id)

def get_study_data():
    url = 'https://www.clinicaltrials.gov/study/REPLACE_NCTID?tab=table#recruitment-information'
    options = Options()
    options.headless = True
    # Using Dataframe to write to xls
    df = pd.DataFrame(columns=('study_id', 'ActualEnrollment', 'OriginalEnrollment',
                               'StudyStartDate','StudyCompletionDate','CurrentStudySponsor','OriginalStudySponsor','Collaborators'))
    # Start Chrome WebDriver
    for nct_id in study_ids:
        # print("nct_id:: ",nct_id)
        study_url = url.replace('REPLACE_NCTID',nct_id)
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
            if 'Collaborators' in section.text :
                dict[section.text] = -1
                name = section.text
                get_next_section = True


        actual_val,estimated_val = -1,-1
        start_date,com_date,current_sponsor,orig_sponsor,collaborators= '','','','',''
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
            elif 'Collaborators' in key:
                collaborators = value

        # print('study_id: ', nct_id," Actual: ",actual_val, " Estimated: ",estimated_val)
        # print('StudyStartDate: ', start_date, " StudyCompletionDate: ", com_date, " CurrentStudySponsor: ", current_sponsor, "OriginalStudySponsor:",orig_sponsor )
        # print('Collaborators: ',collaborators)
        if actual_val != -1 and estimated_val != -1:
            # print(actual_val, estimated_val)
            new_row = {'study_id':nct_id,'ActualEnrollment':actual_val,'OriginalEnrollment':estimated_val,
                       'StudyStartDate':start_date, 'StudyCompletionDate':com_date, 'CurrentStudySponsor':current_sponsor,
                       'OriginalStudySponsor':orig_sponsor,'Collaborators':collaborators}
            df.loc[len(df)] = new_row
        else:
            print("**"*10)
            print("Error:: Data not entered for id: ",nct_id)
            print("Values in dict: ",dict)
        time.sleep(1)
    df.to_excel("output.xlsx")

def cal_diff():
    if os.path.exists("./output.xlsx"):
        excel_data_df = pd.read_excel("./output.xlsx", dtype=str,index_col=0)
        excel_data_df['difference'] =  excel_data_df.apply(lambda x: int(x['ActualEnrollment']) - int(x['OriginalEnrollment']) if x['OriginalEnrollment'] != 'Same as current' and str(x['ActualEnrollment']) != 'Same as current' else 0,axis=1)
        excel_data_df.style.apply(lambda x:(None,None,None,None,None,None,None,None,'background-color: green') if x['difference'] >=0 else (None,None,None,None,None,None,None,None,'background-color: red'), axis=1).to_excel("./new_output.xlsx")
    else:
        print("File does not exist")

def valid_date(date_string):
    # check for valid dates in (MM/DD/YYYY) format
    try:
        return datetime.strptime(date_string, "%m/%d/%Y")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date: '{date_string}'. Expected format: MM/DD/YYYY.")

#python cts_scraping.py "Bristol-Myers" 01/01/2024 06/12/2024
if __name__ == "__main__":
    # Will be passed from cmdline
    parser = argparse.ArgumentParser(description="Fetch and export clinical trial studies data to Excel.")
    parser.add_argument('sponsor', type=str, help='The sponsor name for filtering clinical studies.')
    parser.add_argument('start_date', type=valid_date, help='The start date in MM/DD/YYYY format.')
    parser.add_argument('end_date', type=valid_date, help='The end date in MM/DD/YYYY format.')
    args = parser.parse_args()

    # sponsor_name = "Bristol-Myers"  # Example sponsor
    # start_date = "06/01/2024"  # Example start date
    # end_date = "06/12/2024"  # Example end date

    print(args.sponsor, args.start_date.strftime("%m/%d/%Y"), args.end_date.strftime("%m/%d/%Y"))
    get_study_ids(args.sponsor, args.start_date.strftime("%m/%d/%Y"), args.end_date.strftime("%m/%d/%Y"))
    print("Total study ids: ", len(study_ids))
    # print(study_ids)
    if len(study_ids) > 0:
        get_study_data()
        cal_diff()
