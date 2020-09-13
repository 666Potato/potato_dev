import os
import random
import time

from PIL import Image, ImageDraw, ImageFont
from celery import shared_task

from pyquery import PyQuery as pq
import requests

from lessons.models import Articles

SPONSOR_LABELS = ('sponsor', 'podcast', 'video')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        # Check for sponsor and make sure that description has no a tags
        if a_tag is not None and is_item_title:
            if desc_i < len(article_blocks):
                if pq(article_blocks[desc_i]).children():
                    continue
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


def generate_image(article_author):
    # Random colors
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rgb = tuple([r, g, b])

    # Generating background image
    background = Image.new('RGBA', (960, 640), color=rgb)

    # Getting default image for course
    image = Image.open(os.path.join(BASE_DIR, 'resources/bg-course.png'))
    resized_image = image.resize((round(image.size[0]*0.7), round(image.size[1]*0.7)))

    # Generating background color for default image
    bg_main = Image.new('RGBA', (resized_image.size[0], resized_image.size[1]), color=(195, 140, 238))
    bg_main.paste(resized_image, (0, 0), resized_image)

    # Calculating x, y for top left corner of default image
    offset = (round(background.size[0]/2 - bg_main.size[0]/2), background.size[1] - bg_main.size[1])

    background.paste(bg_main, offset)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('arial.ttf', 30)
    timestamp = time.localtime()
    ts = time.strftime("%Y-%m-%d", timestamp)
    path = 'uploads/articles/{0}_{1}.png'.format(article_author.split(' ')[0], ts)
    filepath = os.path.join(BASE_DIR, path)
    # Getting w, h of the text and calculating positions of x, y for text
    w, h = font.getsize(article_author)
    draw.text(((background.size[0] - w)/2, round(background.size[1]*0.3)),
              'Published by {0}'.format(article_author), font=font)

    background.save(filepath)

    return filepath


@shared_task
def articles_to_db():
    articles = pycoders_articles()
    for article in articles:
        article_image = generate_image(article['author'])
        Articles.objects.get_or_create(title=article['title'], link=article['link'],
                                       desc=article['desc'], author=article['author'], image=article_image)
