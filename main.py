import json
import requests
import xlsxwriter
from datetime import datetime


url_1 = 'https://classic.clinicaltrials.gov/api/query/full_studies'
url_2 = 'https://classic.clinicaltrials.gov/api/info/study_structure'
url_3 = 'https://classic.clinicaltrials.gov//api/info/study_statistics'
url_4 = 'https://ClinicalTrials.gov/api/query/full_studies?'
url_5 = 'https://www.clinicaltrials.gov/study/NCT01714739'
# keyword = 'heart attack'
# filename =  datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ".xlsx"

resp = requests.get(url_1,params={'expr':'AREA[CompletionDate]RANGE[06/01/2024, 06/12/2024]','max_rnk':50,'fmt':'json','fields':['NCTId','StudyFirstSubmitQCDate','ResultsFirstPostDate','OverallStatus','history']})
# resp = requests.get(url_5,params={'max_rnk':3,'fmt':'json','fields':['NCTId','StudyFirstSubmitQCDate','ResultsFirstPostDate','OverallStatus','history']})

if resp.status_code == 200:
    study_resp = json.loads(resp.text)
    max_studies = study_resp['FullStudiesResponse']['NStudiesFound']
    total_studies_read = study_resp['FullStudiesResponse']['NStudiesReturned']
    print("total_studies_read: ",total_studies_read)
    print("max_studies::",max_studies)
    print("")
    # len_studies = study_resp['FullStudiesResponse']['FullStudies']
    for item in study_resp['FullStudiesResponse']['FullStudies']:
        ncti_id = item['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        enrollment_number = item['Study']['ProtocolSection']['DesignModule']['EnrollmentInfo']['EnrollmentCount']
        enrollment_type = item['Study']['ProtocolSection']['DesignModule']['EnrollmentInfo']['EnrollmentType']
        print(ncti_id,enrollment_number,enrollment_type)

    # if max_studies > 100:
    #     inc = 100
    #     for i in range(100,max_studies,inc):
    #         print(i)
    #         try:
    #             resp = requests.get(url_1,
    #                                 params={'expr': 'AREA[CompletionDate]RANGE[06/01/2024, 06/12/2024]',
    #                                         'min_rnk' : total_studies_read,
    #                                         'max_rnk': i,
    #                                         'fmt': 'json',
    #                                         'fields': ['NCTId', 'StudyFirstSubmitQCDate', 'ResultsFirstPostDate',
    #                                                    'OverallStatus']})
    #             resp.raise_for_status()
    #             if resp.status_code == 200:
    #                 study_resp = json.loads(resp.text)
    #                 total_studies_read = total_studies_read + study_resp['FullStudiesResponse']['NStudiesReturned']
    #                 print("total_studies_read: ", total_studies_read)
    #                 if max_studies - total_studies_read > 100:
    #                     inc = 100
    #                 else:
    #                     inc =  max_studies - total_studies_read
    #             else:
    #                 print("Error: ", resp.status_code)
    #         except requests.exceptions.HTTPError as errh:
    #             print("HTTP Error")
    #             print(errh.args[0])
    #
    #     print("total_studies_read: ",total_studies_read)

else:
    print("Error: ",resp.status_code)

