from __future__ import unicode_literals

from celery import shared_task
from potato_dev.celery import app
from celery.schedules import crontab
from pyquery import PyQuery as pq
import requests

from lessons.models import Articles

SECONDS_IN_DAY = 60 * 60 * 24
SPONSOR_LABELS = ['sponsor', 'podcast', 'video']


@shared_task
def last_articles(count=3):
    """ Method returns last articles from pycoders.com. Standard is three """
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

    # Write to db
    print('repeated\n----', articles[:count])
    # Pycoders updates every Monday. Day of writing func is Saturday, therefore + two days.
    # Once launched in deployment, needs adjustment
    new_or_created = []
    for article in articles[:3]:
        new_or_created.append(Articles.objects.get_or_create(title=article['title'], link=article['link'],
                                                             desc=article['desc'], author=article['author']))
    return new_or_created


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        last_articles.s(),
    )