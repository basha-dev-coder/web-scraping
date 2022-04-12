import re

from bs4 import BeautifulSoup
import requests
import pandas as pd

job_name = input(r"Enter your job title to search: ").replace(' ', '-')
job_name = job_name.lower().replace(' ', '-')
baseURL = f'https://www.reed.co.uk/jobs/{job_name}-jobs'

response = requests.get(baseURL)
# print(response)

soup = BeautifulSoup(response.text, "html.parser")
job_cards = soup.find_all("article", class_=re.compile('job-result'))
print(f"Total jobs are {len(job_cards)}")
job_df = pd.DataFrame(columns=['Title', 'Posted-On', 'Company', 'Salary', 'Location', 'Remote/Office', 'Time'])
print(job_df)
for i, job_card in enumerate(job_cards):
    job_title = job_card.find("h3", class_='title').a
    job_posted_by = job_card.find("div", class_='posted-by')
    job_salary = job_card.find("li", class_="salary")
    job_location = job_card.find("li", class_="location")
    job_remote = job_card.find("li", class_="remote")
    job_time = job_card.find("li", class_="time")

    job_title_text = job_title if job_title is None else job_title.get_text().strip()
    job_posted_by_text = job_posted_by if job_posted_by is None else job_posted_by.get_text().strip()
    job_posted_by_text = job_posted_by_text.split('by')[0].split('Posted')[1].strip()
    job_company_text = job_posted_by if job_posted_by is None else job_posted_by.a.get_text().strip()
    job_salary_text = job_salary if job_salary is None else job_salary.get_text().strip()
    job_location_text = job_location if job_location is None else job_location.get_text().strip()
    job_remote_text = job_remote if job_remote is None else job_remote.get_text().strip()
    job_time_text = job_time if job_time is None else job_time.get_text().strip()

    list_df = [job_posted_by_text, job_company_text, job_salary_text, job_location_text, job_remote_text, job_time_text]
    job_df = pd.concat(pd.Series(list_df, index=job_df.columns[:len(list_df)]), job_df, ignore_index=True)

    print(f'job title is {job_title_text}')
    print(f'job posted by on {job_posted_by_text}')
    print(f'job company by {job_company_text}')
    print(f'job salary is {job_salary_text}')
    print(f'job location is {job_location_text}')
    print(f'job remote is {job_remote_text}')
    print(f'job time is {job_time_text}')

print(job_df.head())
