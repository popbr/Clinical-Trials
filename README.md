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
