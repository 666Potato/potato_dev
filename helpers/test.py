from bs4 import BeautifulSoup

import requests


def get_articles():

    r = requests.get('https://pycoders.com/issues')
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    div_element = soup.find('div', {'class': 'mb-3'})
    a_list = div_element.find_all('a')
    link = 'https://pycoders.com'

    for item in a_list[:1]:
        link += item.get('href')

    r = requests.get(link)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    spans = soup.find_all('h2')[3].find_next_siblings('span')

    author_list = [spans[2].string, spans[5].string, spans[8].string]
    topic_list = [spans[0].string, spans[3].string, spans[6].string]
    topic_links_list = [spans[0].find('a').get('href'), spans[3].find('a').get('href'), spans[6].find('a').get('href')]
    topic_desc_list = [spans[1].string, spans[4].string, spans[7].string]

    return author_list, topic_list, topic_links_list, topic_desc_list
