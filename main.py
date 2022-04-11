from bs4 import BeautifulSoup
import requests
import pandas as pd

baseURL = 'https://www.amazon.co.uk/'

response = requests.get(baseURL)
print(response)

soup = BeautifulSoup.get(response)