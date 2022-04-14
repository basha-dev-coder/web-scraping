import re

from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st

st.title('Dream job Finder')

job_name = st.text_input('Enter your dream job', value='data analyst')
job_name = job_name.lower().replace(' ', '-')
baseURL = 'https://www.reed.co.uk'
jobs_baseURL = f'{baseURL}/jobs/{job_name}-jobs'

response = requests.get(jobs_baseURL)
# print(response)

soup = BeautifulSoup(response.text, "html.parser")
job_cards = soup.find_all("article", class_=re.compile('job-result'))
print(f"Total jobs are {len(job_cards)}")
columns = ['Title', 'Posted-On', 'Company', 'Salary', 'Min Salary', 'Max Salary', 'Salary based on', 'Location',
           'Remote/Office', 'Type', 'Time', 'More Info']
job_df = pd.DataFrame(data=None, columns=columns)
print(job_df)


def get_min_max_salary(salary_text, term):
    if len(salary_text.split('-')) == 2:
        minsalary = salary_text.split('-')[0].strip()
        maxsalary = salary_text.split('-')[1].split('per annum')[0].strip()
    else:
        minsalary = salary_text.split('per annum')[0].strip()
        maxsalary = salary_text.split('per annum')[0].strip()
    return minsalary, maxsalary


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
    job_location_text = job_location_text.split('\n')[0].strip()
    job_remote_text = job_remote if job_remote is None else job_remote.get_text().strip()
    job_time_text = job_time if job_time is None else job_time.get_text().strip()
    job_type_text = job_time_text if job_time_text is None else job_time_text.split(',')[0].strip()
    job_time_text = job_time_text if job_time_text is None else job_time_text.split(',')[1].strip()

    job_moreinfo_link = baseURL + job_title['href'] if job_title['href'].startswith('/') else job_title['href']

    if 'per day' in job_salary_text:
        salary_based_on = 'per day'
        min_salary, max_salary = get_min_max_salary(job_salary_text, salary_based_on)
    elif 'per annum' in job_salary_text:
        salary_based_on = 'per annum'
        min_salary, max_salary = get_min_max_salary(job_salary_text, salary_based_on)
    elif 'per hour' in job_salary_text:
        salary_based_on = 'per hour'
        min_salary, max_salary = get_min_max_salary(job_salary_text, salary_based_on)
    else:
        # this is for competitive/ Salary negotiable text for salary
        min_salary = None
        max_salary = None
        salary_based_on = None


    list_df = [job_title_text, job_posted_by_text, job_company_text, job_salary_text, min_salary, max_salary,
               salary_based_on, job_location_text, job_remote_text, job_type_text, job_time_text, job_moreinfo_link]
    # temp_df = pd.DataFrame([list_df], columns=columns)
    # job_df = job_df.append(temp_df, ignore_index=True)

    job_df.loc[i, :] = list_df

print(job_df.head())
st.write(job_df.shape)
