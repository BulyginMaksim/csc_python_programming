from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random

name = "Python blog tracker"
version = "0.1"
depends = ['beatifulsoup4']
waiter = True


def get_news():
    url = "https://www.python.org/blogs/"
    data = urlopen(url).read().decode('utf8')
    bs = BeautifulSoup(data, features="html.parser")

    date = bs.find(
        'ul', class_='list-recent-posts').li.p.time.attrs['datetime']
    title = bs.find(
        'ul', class_='list-recent-posts').li.h3.text.replace('!', '')\
                                         .replace('.', '')

    if datetime.datetime.strptime(date, '%Y-%m-%d').day == \
       datetime.date.today().day \
       and \
       datetime.datetime.strptime(date, '%Y-%m-%d').month == \
       datetime.date.today().month:
        return {'title': 'New post in Python blog!',
                'text': f'It\'s titled "{title}". '
                        f'Check it out on python.org/blogs/ now!'}
    return None
