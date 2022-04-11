from bs4 import BeautifulSoup
import requests
import pandas as pd

baseURL = 'https://www.amazon.co.uk/'

response = requests.get(baseURL)
print(response.text)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.find_all('a'))
