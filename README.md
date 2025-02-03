# Clinical Trials

## Introduction

This project processes clinical data from https://clinicaltrials.gov/, specifically focusing on returning estimated or actual enrollment for studies. It can also search for studies within a specific date range. This project can be used as a tool for analyzing trends, assessing study participation, and gaining insights into the scale of clinical trials over time. The project was developed using [PyCharm](https://www.jetbrains.com/pycharm/).

## Walkthrough

1)  Import all necessary libraries (`BeautifulSoup`, `webdriver`, `pandas`).
2)  Create a list of study IDs containing the specific identifiers for each study (e.g., 'NCT01714739', 'NCT05844007').
3)  Set up Chrome WebDriver for headless browsing.
4)  Loop through each `nct_id` in the study IDs list.
5)  For each ID, generate the specific URL and use Selenium to load the page.
6)  Parse the HTML page with BeautifulSoup to find the section about enrollment information.
7)  Extract and return the estimated/actual enrollment.
8)  Save the data to an Excel file (`output.xlsx`).
9)  In the Excel sheet, add a column that calculates the difference between the actual and estimated enrollment.
10) Export the final Excel file.

## Set up

### For Windows Beginners
1) Find the repository in File Explorer (look for a folder called clinical-trials and contains this file) once found click on the search bar on the top press ctrl + c to copy the path to the repository (It should start with C: )
2) Open Windows PowerShell
3) Type these commands including any spaces but not including brackets
```py
cd [PathToRepository] # this takes power shell to where the files you want to run are stored
python -m venv venv # this opens up a virtual environment
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process # this allow you to run scripts the -scope process part means the execution policy will one be unresticted for the instance of powershell meaning when you close out or open a new tab in powershell it will return to normal
.\venv\Scripts\activate #now you will be running scripts
py -m pip install --upgrade pip # if it says requirment already satisified after typeing this that is fine
py -m pip install -r requirements.txt # installs requirments for program
py -i cts_scraping.py "Bristol-Myers" 01/01/2023 06/12/2024 # this will actually run the program follow the format -i cts_scraping.py "[NameOfAuthor]" [StartDate] [EndDate]
# note that the particular example above will take a while to run, about several minutes
```
3) open the output file in the clinical trials folder and it should have all the data filled in

### For Linux experts

```
python3 -m venv venv
venv/bin/pip install -r requirements.txt 
venv/bin/python -i cts_scraping.py "Bristol-Myers" 01/01/2024 06/12/2024
```
