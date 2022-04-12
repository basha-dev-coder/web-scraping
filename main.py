import re

from bs4 import BeautifulSoup
import requests
import pandas as pd

baseURL = 'https://www.reed.co.uk/jobs/software-developer-jobs'

response = requests.get(baseURL)
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.find_all('a'))
job_card = soup.find("article", class_=re.compile('job-result'))
print(job_card)
job_title = job_card.find("h3", class_='title').a.get_text()
job_posted_by = job_card.find("div", class_='posted-by').get_text()
job_salary = job_card.find("li", class_="salary").get_text()
job_location = job_card.find("li", class_="location").get_text()
job_remote = job_card.find("li", class_="remote").get_text()
job_time = job_card.find("li", class_="time")

print(f'job title is {job_title.strip()}')
print(f'job posted by is {job_posted_by.strip()}')
print(f'job salary is {job_salary.strip()}')
print(f'job location is {job_location.strip()}')
print(f'job remote is {job_remote.strip()}')
print(f'job time is {job_time}')
