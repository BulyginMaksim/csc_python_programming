import requests
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup

name = "RoboCorona"
version = "0.12"
depends = ['bs4']
waiter = False


def get_page(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find('div', class_='layout-four')
    return None


def get_data(all_news):
    if all_news:
        cases_elem = all_news.find(text=re.compile(r'.*Случа.*')).parent
        cases_b = cases_elem.find('b')
        total_str = cases_b.find(text=True)        # число случаев
        delta_str = cases_b.find('span').text[1:]  # прирост
        return total_str, delta_str
    return None, None


def get_text_news(total, delta):
    date_now = datetime.now().date().strftime("%D")
    title, text_news = None, None
    if total and int(delta) > 0:
        title = [
            f'Количество заражений COVID-19 в Санкт-Петербурге '
            f'увеличилось на {delta}!',

            f'В Санкт-Петербурге увеличилось количество '
            f'заражений короновирусом!',

            f'В Питере выросло число случаев заражений '
            f'короновирусом на {delta}!',

            f'+{delta} новых случаев обнаружения короносируса в '
            f'Санкт-Петербурге!',

            f'Короновирус не отступает! Число случаев заражений '
            f'COVID-19 выросло'
        ]

        text_news = [
            f'В Санкт-Петербурге число случаев '
            f'заражения короновирусом на сегодняшний день '
            f'составляет {total}, новых случаев  выявлено {delta}!',

            f'На сегодня {date_now} в Санкт-Петербурге '
            f'зафиксировано {delta} новых случаев заражения! '
            f'Общее их количество составляет {total}.',

            f'В Санкт-Питербурге увеличилось число выявленных '
            f'случаев заражения COVID-19 на {delta}. '
            f'На дату {date_now} всего {total} случаев заражений',

            f'Увеличение выявленных случаев заражений на {delta} '
            f'в  Санкт-Питербрге удивляет! Всего случаев уже '
            f'{total}!',

            f'Сегодня {date_now} были выявлены новые случаи заражений '
            f'COVID-19 в культурной столице. Статистика показывает '
            f'{delta} новых случаев!'
        ]
    elif total:
        title = [
            f'Количество заражений COVID-19 на сегодня в Санкт-Петербурге '
            f'не изменилось.',

            f'В Санкт-Петербурге нет прироста количества заражений '
            f'короновирусом!',

            f'Короновирус отступает? В Санкт-Петербурге не выявлено '
            f'новых случаев заражений COVID-19'
        ]

        text_news = [
            f'В Санкт-Петербурге число случаев заражения короновирусом '
            f'на сегодняшний день составляет {total}, новых случаев '
            f'не выявлено!',

            f'На сегодня {date_now} в Санкт-Петербурге не зафиксировано '
            f'новых случаев заражения! Общее их количество '
            f'составляет {total}.',

            f'В Санкт-Питербурге не увеличилось число выявленных случаев '
            f'заражения COVID-19, что удивляет. На дату {date_now} всего '
            f'{total} случаев заражений.',

            f'Неизменение выявленных случаев заражений в Санкт-Питербрге '
            f'удивляет! Всего случаев {total}, как и вчера!',

            f'Сегодня {date_now} не были выявлены новые случаи заражений '
            f'COVID-19 в культурной столице. Статистика показывает {total} '
            f'случаев!'
        ]
    return title, text_news


def get_news():
    all_news = get_page(
        'https://coronavirus-control.ru/coronavirus-saint-petersburg/'
    )
    total, delta = get_data(all_news)
    title, text_news = get_text_news(total, delta)
    if title:
        return {'title': random.choice(title),
                'text': random.choice(text_news)}
    return None
