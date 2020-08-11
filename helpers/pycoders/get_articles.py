from bs4 import BeautifulSoup

import requests


def get_articles():
    r = requests.get('https://pycoders.com/issues')
    text = r.text
    soup = BeautifulSoup(text)
    div_element = soup.find('div', {'class': 'mb-3'})
    a_list = div_element.find_all('a')
    link = 'https://pycoders.com/'

    for item in a_list[:1]:
        link = item.get('href')

    print(link)
