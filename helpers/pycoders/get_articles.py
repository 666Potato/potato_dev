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
    all_blocks = d('body').find('h2:contains("Articles")').nextAll()

    article_blocks = []
    for article_block in all_blocks:
        if article_block.tag != 'h2':
            if article_block.tag == 'span':
                article_blocks.append(article_block)
        else:
            break

    articles = []
    i = 0
    for item in article_blocks:

        a_tag = item.find('a')
        if a_tag is not None and 'font-size: 20px' in item.get('style') and article_blocks[i+9].text != 'sponsor':
            link = a_tag.get('href')
            title = a_tag.text
            # print(title)
            print(article_blocks[i+9].text == 'sponsor')

        else:
            if 'font-size:16px' in item.get('style') and item.find('a') is None:
                desc = item.text

            if item.find('a') is not None and 'color: #AAAAAA' in item.get('style') and article_blocks[i].text is None:
                author = item.find('a').text
                article = {'link': link, 'title': title, 'desc': desc, 'author': author}
                articles.append(article)
    i += 1

    print(articles)
    return articles


if __name__ == '__main__':
    last_three_articles()
