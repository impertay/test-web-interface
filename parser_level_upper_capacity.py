import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def get_level_upper_capacity(html):
    soup = BeautifulSoup(html, 'lxml')
    level_upper_capacity = soup.find('div', id='upper_capacity_level').get('style')
    number_level_upper_capacity = level_upper_capacity.split(' ')[1].split('%')[0]
    return int(number_level_upper_capacity)

def parser_level_upper_capacity():
    url = 'http://50d1c16b.ngrok.io'
    level_upper_capacity = get_level_upper_capacity(get_html(url))
    if level_upper_capacity > 40:
        return 'Уровень привышен'
    else:
        return level_upper_capacity
