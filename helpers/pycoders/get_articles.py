from pyquery import PyQuery as pq
import requests

SECONDS_IN_DAY = 60 * 60 * 24


def last_three_articles():
    r = requests.get('https://pycoders.com/issues')
    d = pq(r.text)
    a = d('.mb-3').find('a').attr('href')
    last_issue = 'https://pycoders.com' + a

    r = requests.get(last_issue)
    d = pq(r.text)
    tag = d('body').find('h2:contains("Projects")')
    all_blocks = d('body').find('h2:contains("Articles")').nextAll()
    article_blocks = []

    for article_block in all_blocks:
        if article_block.tag != 'h2':
            if article_block.tag == 'span':
                article_blocks.append(article_block)
        else:
            break

    articles = []
    for item in article_blocks:

        a_tag = item.find('a')
        if a_tag is not None and 'font-size: 20px' in item.get('style'):
            link = a_tag.get('href')
            title = a_tag.text
            article = {'link': link, 'title': title, 'desc': article_blocks[1].text}
            articles.append(article)

    print(articles)
    return articles


print(__name__)
if __name__ == '__main__':
    last_three_articles()

    # soup = BeautifulSoup(r.text, 'html.parser')
    # div_element = soup.find('div', {'class': 'mb-3'})
    # a_list = div_element.find_all('a')
    # link = 'https://pycoders.com'
    #
    # for item in a_list[:1]:
    #     link += item.get('href')
    #
    # r = requests.get(link)
    # text = r.text
    # soup = BeautifulSoup(text, 'html.parser')
    # spans = soup.find_all('h2')[3].find_next_siblings('span')
    #
    # author_list = [spans[2].string, spans[5].string, spans[8].string]
    # topic_list = [spans[0].string, spans[3].string, spans[6].string]
    # topic_links_list = [spans[0].find('a').get('href'), spans[3].find('a').get('href'), spans[6].find('a').get('href')]
    # topic_desc_list = [spans[1].string, spans[4].string, spans[7].string]
    #
    # return author_list, topic_list, topic_links_list, topic_desc_list

