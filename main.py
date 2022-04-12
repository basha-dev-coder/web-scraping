import re

from bs4 import BeautifulSoup
import requests
import pandas as pd

baseURL = 'https://www.reed.co.uk/jobs/software-developer-jobs'

response = requests.get(baseURL)
print(response)

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.find_all('a'))
job_cards = soup.find_all("article", class_=re.compile('job-result'))
# print(job_cards)
for job_card in job_cards:
    # print(job_card.find("h3", class_='title').a)
    job_title = job_card.find("h3", class_='title').a
    # print(job_title is None)
    job_posted_by = job_card.find("div", class_='posted-by')
    job_salary = job_card.find("li", class_="salary")
    job_location = job_card.find("li", class_="location")
    job_remote = job_card.find("li", class_="remote")
    job_time = job_card.find("li", class_="time")

    print(f'job title is {job_title if type(job_title) is not None else job_title.gettext().strip()}')
    print(f'job posted by is {job_posted_by if job_posted_by is not None else job_posted_by.gettext().strip()}')
    print(f'job salary is {job_salary if job_salary is not None else job_salary.gettext().strip()}')
    print(f'job location is {job_location if job_location is not None else job_location.gettext().strip()}')
    print(f'job remote is {job_remote if job_remote is not None else job_remote.gettext().strip()}')
    print(f'job time is {job_remote if job_remote is not None else job_time.gettext().strip()}')
