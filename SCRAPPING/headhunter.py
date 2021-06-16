import requests
import unicodedata
from bs4 import BeautifulSoup

import requests

from bs4 import BeautifulSoup

ITEMS = 100
URL = f'https://hh.kz/search/vacancy?st=searchVacancy&text=java&items_on_page={ITEMS}'
##'https://hh.kz/search/vacancy?items_on_page=100&st=searchVacancy&text=java'

headers = { 
  'Host': 'hh.kz',
  'User-Agent': 'Chrome',
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

def extract_max_page():
  hh_request = requests.get(URL, headers=headers)
  hh_soup = BeautifulSoup(hh_request.text, 'html.parser')
  pages = []
  paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
  for page in paginator:
    pages.append(int(page.find('a').text))
  #return pages[-1]
  return 1

def extract_job(html):
  title = html.find('a').text
  link = html.find('a')['href']
  company =  unicodedata.normalize('NFKC',html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text)
  company = company.strip()
  location =  unicodedata.normalize('NFKC',html.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text)
  location = location.partition(',')[0]
  return {'title': unicodedata.normalize('NFKC',title), 'company': unicodedata.normalize('NFKC',company), 'location': unicodedata.normalize('NFKC',location), 'link': unicodedata.normalize('NFKC',link)}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f'Headhunter: парсинг страницы {page}')
    result = requests.get(f'{URL}&page={page}', headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
  

def get_jobs():
  max_page = extract_max_page()
  jobs = extract_jobs(max_page)
  return jobs



