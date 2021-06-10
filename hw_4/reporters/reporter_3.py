from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

name = "Dilbert tracker"
version = "0.1"
depends = ['beatifulsoup4']
waiter = True


def get_news():
    url = "https://dilbert.com"
    data = urlopen(url).read().decode('utf8')
    bs = BeautifulSoup(data, features="html.parser")
    date = bs.find('div', class_='js-comics')\
        .findChildren(recursive=False)[0].find('h2').a.find('date').span.text

    if datetime.datetime.strptime(date, '%A %B %d,').day == \
       datetime.date.today().day \
       and \
       datetime.datetime.strptime(date, '%A %B %d,').month == \
       datetime.date.today().month:
        return {'title': 'New Dilbert comics is here!',
                'text': 'Check it out on dilbert.com now!'}
    return None
