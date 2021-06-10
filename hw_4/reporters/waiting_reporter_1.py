import datetime
import logging
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from requests import TooManyRedirects, RequestException

name = "Neputin"
version = "0.0.2"
depends = ['requests', 'bs4']
waiter = True
country = "Россия"
president_ru = "Владимир Путин"
president_en = "Vladimir Putin"


def get_news():
    import requests

    # запрос в гугл для получения текущего президента РФ
    # с правильно указанным браузером (User-Agent) можно
    # получить имя президента
    # в специальном прямоугольничке, который легко распарсить,
    # поэтому я указываю в header-е своего агента
    url = f"http://www.google.com/search?q=президент+{country}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/527.16 (KHTML, like Gecko) '
                      'Chrome/81.0.4032.13 Safari/735.12'}

    try:
        # получаем html-страницу с прямоугольником,
        # где указан текущий президент РФ
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        data = response.text

        soup = BeautifulSoup(data, 'html.parser')
        president = soup.find("a", {"class": "FLP8od"}).contents[0]

        # раскомментируйте строку ниже, чтобы увидеть текущего президента
        # print(president)

        president_names = {president_ru, president_en}

        if president in president_names:
            current_year = datetime.datetime.now().year
            years = (2008 - 2000) + (current_year - 2012)

            return {
                'title': f'{president_ru} больше не у власти!',
                'text': f'{president_ru} покинул пост Президента '
                        f'страны {country} после {years} лет '
                        f'правления! Его сменил {president}.'
            }
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
