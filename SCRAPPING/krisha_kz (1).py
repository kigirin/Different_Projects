import requests
import csv
from bs4 import BeautifulSoup
import io

URL_apartments = 'https://krisha.kz/prodazha/kvartiry/'
URL_houses = 'https://krisha.kz/prodazha/doma/'
URL_dacha = 'https://krisha.kz/prodazha/dachi/'
URL_area = 'https://krisha.kz/prodazha/uchastkov/'
URL_offices = 'https://krisha.kz/prodazha/ofisa/'
URL_rooms = 'https://krisha.kz/prodazha/pomeshhenija/'
URL_buildings = 'https://krisha.kz/prodazha/zdanija/'
URL_shops = 'https://krisha.kz/prodazha/magazina/'
URL_bases = 'https://krisha.kz/prodazha/prombazy/'
URL_others = 'https://krisha.kz/prodazha/prochej-nedvizhimosti/'
URL_foreign = 'https://krisha.kz/prodazha/zarubezhnoj-nedvizhimosti/'

HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
          'accept':'*/*'}
HOST = 'https://krisha.kz/'
FILE_apartments = 'apartments.csv'
FILE_houses = 'houses.csv'
FILE_dacha = 'dacha.csv'
FILE_offices = 'offices.csv'
FILE_area = 'area.csv'
FILE_buildings = 'buildings.csv'
FILE_bases = 'bases.csv'
FILE_rooms = 'rooms.csv'
FILE_shops = 'shops.csv'
FILE_foreign = 'foreign.csv'
FILE_others = 'others_k.csv'


def get_html(url, params=None):
    r=requests.get(url, headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='paginator__btn')
    if pagination:
        return 1
        #return int(pagination[-2].get_text())
    else:
        return 1

def save_file(items, path):
    with io.open(path, 'w', newline='', errors='ignore') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Title', 'Link', 'City', 'Address', 'Price', 'Details', 'New building', 'New Building info'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['city'], item['address'], item['price'], item['details'],
                             item['new_building'], item['new_building_info']])

def exception_handling(item):
    if item:
        item = item.get_text(strip = True)
    else:
        item='NaN'
    return item

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="a-card")
    houses=[]
    for item in items:
        new_building = item.find("div", class_="a-card__complex-info")
        new_building_info = ''
        if new_building:
            new_building=True
            new_building_info = item.find("div", class_="a-card__complex-info").find_next('a').get_text(strip=True)
        else:
            new_building = False
            new_building_info = 'Not a new building'

        title = exception_handling(item.find("a", class_="a-card__title"))
        link = item.find("a", class_="a-card__title")
        if link:
            link = link.get('href')
        else:
            link = 'NaN'

        city = exception_handling(item.find('div', class_='card-stats').find_next('div'))
        address=exception_handling(item.find('div', class_='a-card__subtitle'))
        price=exception_handling(item.find('div', class_='a-card__price'))
        details=exception_handling(item.find('div', class_='a-card__text-preview'))
        houses.append({
            'title':title,
            'link':HOST + link,
            'city': city,
            'address': address,
            'price': price.replace(u'\xa0', u' '),
            'details': details,
            'new_building': new_building,
            'new_building_info': new_building_info,
        })
    return houses


def execution(html, FILE):
    if html.status_code == 200:
        get_content(html.text)
        houses=[]
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f"Parsing page {page} from {pages_count}...")
            html = get_html(URL_apartments, params={'page':page})
            houses.extend(get_content(html.text))
        save_file(houses, FILE)
        print(f"{len(houses)} advertisements was get")
    else:
        print('Error')

def parse():
    html_apartments = get_html(URL_apartments)
    html_houses = get_html(URL_houses)
    html_dacha = get_html(URL_dacha)
    html_offices = get_html(URL_offices)
    html_area = get_html(URL_area)
    html_buildings = get_html(URL_buildings)
    html_bases = get_html(URL_bases)
    html_rooms = get_html(URL_rooms)
    html_shops = get_html(URL_shops)
    html_foreign = get_html(URL_foreign)
    html_others = get_html(URL_others)

    print('Parsing apartments:')
    execution(html_apartments, FILE_apartments)
    print('Parsing houses:')
    execution(html_houses, FILE_houses)
    print('Parsing dacha:')
    execution(html_dacha, FILE_dacha)
    print('Parsing offices:')
    execution(html_offices, FILE_offices)
    print('Parsing areas:')
    execution(html_area, FILE_area)
    print('Parsing buildings:')
    execution(html_buildings, FILE_buildings)
    print('Parsing bases:')
    execution(html_bases, FILE_bases)
    print('Parsing rooms:')
    execution(html_rooms,FILE_rooms)
    print('Parsing shops:')
    execution(html_shops, FILE_shops)
    print('Parsing foreign:')
    execution(html_foreign, FILE_foreign)
    print('Parsing others:')
    execution(html_others, FILE_others)

parse()
