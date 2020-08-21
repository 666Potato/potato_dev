from __future__ import unicode_literals

from celery import shared_task
from pyquery import PyQuery as pq
import requests

from lessons.models import Articles

SPONSOR_LABELS = ['sponsor', 'podcast', 'video']


def pycoders_articles():
    """ Method returns last articles from pycoders.com. """
    req = requests.get('https://pycoders.com/issues')
    html_snapshot = pq(req.text)
    a_source = html_snapshot('.mb-3').find('a').attr('href')
    last_issue = '{0}{1}'.format('https://pycoders.com', a_source)

    req = requests.get(last_issue)
    html_snapshot = pq(req.text)
    all_blocks = html_snapshot('body').find('h2:contains("Articles")').nextAll()

    # Collect all spans into list between needed section
    article_blocks = []
    for article_block in all_blocks:
        if article_block.tag != 'h2':
            if article_block.tag == 'span':
                article_blocks.append(article_block)
        else:
            break

    # Generate article dict
    articles = []
    for i, item in enumerate(article_blocks):
        desc_i = i + 1
        author_i = i + 2
        sponsor_i = i + 3

        a_tag = item.find('a')
        is_item_title = 'font-size: 20px' in item.get('style')
        # Check for sponsor
        if a_tag is not None and is_item_title:
            if sponsor_i < len(article_blocks):
                if article_blocks[sponsor_i].text in SPONSOR_LABELS:
                    continue

            link = a_tag.get('href')
            title = a_tag.text
            desc = article_blocks[desc_i].text
            author = article_blocks[author_i].find('a').text

            article = {
                'link': link,
                'title': title,
                'desc': desc,
                'author': author,
            }
            articles.append(article)

    return articles


@shared_task
def articles_to_db():
    articles = pycoders_articles()
    for article in articles:
        Articles.objects.get_or_create(title=article['title'], link=article['link'],
                                       desc=article['desc'], author=article['author'])
