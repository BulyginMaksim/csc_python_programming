import logging
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from requests import TooManyRedirects, RequestException

name = "Youtuber"
version = "0.0.1"
depends = ['requests', 'bs4']
waiter = True

# ставим в качестве бейзлайна количество просмотров в 10 миллиардов
# можно менять
limit = 8


def get_news():
    import requests

    # статья с самыми просматриваемыми видео на YouTube
    # здесь есть табличка с топ 30 самыми просматриваемыми видео,
    # она нам и нужна
    url = "https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_videos"

    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')

        tds = [td for td in soup.find_all('td')]
        top_index = -1
        for i in range(len(tds)):
            td = tds[i]
            if len(td.attrs) == 1 and td.get('align') is not None:
                top_index = i
                break

        video_name = tds[top_index + 1].contents[1].text
        channel = tds[top_index + 2].contents[0].text
        views = float(tds[top_index + 3].contents[0])

        if views >= limit:
            return {'title': f'На YouTube появилось первое видео, '
                             f'достигшее более {limit} миллиардов просмотров!',
                    'text': f'Видео с названием "{video_name}", '
                            f'опубликованное каналом с названием "{channel}" '
                            f'на YouTube набрало на данный момент более '
                            f'{views} миллиардов просмотров! Поразительно!'}
    except ConnectionError:
        logging.error('Error occurred with network')
    except HTTPError:
        logging.error('Error occurred while fetching data from API')
    except TooManyRedirects:
        logging.error('Too many redirects')
    except RequestException:
        logging.error('Unknown error occurred')
    except (KeyError, IndexError):
        logging.error('Unexpected HTML tags structure, '
                      'probably it changed since last reporter update')
