import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import csv
URL_CARS="https://kolesa.kz/cars/"
HEADERS={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','accept':'*/*'}
File_CARS='CARS.csv'
URL_Z="https://kolesa.kz/zapchasti/prodazha/?find-in-text=1"
File_Z='Zapchasti.csv'
URL_R="https://kolesa.kz/uslugi/search/?find-in-text=0"
File_R='Repair.csv'
URL_Other="https://kolesa.kz/other/search/?find-in-text=0"
File_Others='Others.csv'
def get_html(url, params=None):
    r=requests.get(url,headers=HEADERS,params=params)

    return r



def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_='pager')
    pager=pagination[0].find_all('li',class_=False)
    if pagination:
        #return int(pager[-1].get_text())
        return 1
    else:
        return 1

def get_content(html):
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('div',class_='a-info-side')

    cars = []
    for item in items:
        try:
            cars.append({
                'title': unicodedata.normalize('NFKC',item.find('span', class_='a-el-info-title').get_text(strip=True)),
                'city': unicodedata.normalize('NFKC',item.find('div', class_='list-region').get_text(strip=True)),
                'date': unicodedata.normalize('NFKC',item.find('span', class_='date').get_text(strip=True)),
                'desc': unicodedata.normalize('NFKC',item.find('div', class_='a-search-description').get_text(strip=True)),
                'price': re.sub("[^0-9]","",str(item.find('span', class_='price').get_text(strip=True)))
                })
        except AttributeError:
            cars.append({
                'title': unicodedata.normalize('NFKC',
                                               item.find('span', class_='a-el-info-title').get_text(strip=True)),
                'city': unicodedata.normalize('NFKC', item.find('div', class_='list-region').get_text(strip=True)),
                'date': unicodedata.normalize('NFKC', item.find('span', class_='date').get_text(strip=True)),
                'desc': unicodedata.normalize('NFKC',
                                              item.find('div', class_='a-search-description').get_text(strip=True)),
                'price': "NaN"
            })

    return cars
def get_content_noPrice(html):
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('div',class_='a-info-side')

    cars = []
    for item in items:
        cars.append({
            'title': unicodedata.normalize('NFKC',item.find('span', class_='a-el-info-title').get_text(strip=True)),
            'city': unicodedata.normalize('NFKC',item.find('div', class_='list-region').get_text(strip=True)),
            'date': unicodedata.normalize('NFKC',item.find('span', class_='date').get_text(strip=True)),
            'desc': unicodedata.normalize('NFKC',item.find('div', class_='a-search-description').get_text(strip=True))
        })

    return cars
def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Title','City','Date','Description','Price in KZT'])
        for item in items:
            try:
                writer.writerow([item['title'],item['city'],item['date'],item['desc'],item['price']])
            except UnicodeError:
                writer.writerow(["NaN","NaN", "NaN", "NaN","NaN"])
def save_file_noPrice(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Title','City','Date','Description'])
        for item in items:
            try:
                writer.writerow([item['title'],item['city'],item['date'],item['desc']])
            except UnicodeError:
                writer.writerow(["NaN", "NaN", "NaN", "NaN"])

def parse(url,file):
    html=get_html(url)
    if html.status_code==200:
        cars=[]
        pages=get_pages_count(html.text)
        print("LOADING...")
        for page in range(1,pages+1):
            html=get_html(url,params={'page':page})
            cars.extend(get_content(html.text))
        save_file(cars,file)
        print('FINISHED')
    else:
        print('Error',file)
def parse_noPRICE(url,file):
    html=get_html(url)
    if html.status_code==200:
        cars=[]
        pages=get_pages_count(html.text)
        print("LOADING...")
        for page in range(1,pages+1):
            html=get_html(url,params={'page':page})
            cars.extend(get_content_noPrice(html.text))
        save_file_noPrice(cars,file)
        print('FINISHED')
    else:
        print('Error',file)

parse(URL_CARS,File_CARS)
#parse(URL_Z,File_Z)
#parse_noPRICE(URL_R,File_R)
#parse_noPRICE(URL_Other,File_Others)