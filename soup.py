import requests
from bs4 import BeautifulSoup

hist_page = 'https://www.clinicaltrials.gov/study/NCT01714739?cond=cancer&aggFilters=status:com&rank=3&tab=history&a=1&b=75#version-content-panel'

resp = requests.get(hist_page)

if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(soup.prettify())
