import json
import requests
import random
import datetime
from bs4 import BeautifulSoup

name = "RodoIlonMask"
version = "0.12"
depends = ['bs4']
waiter = False


def get_data(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        all_news = soup.find('script', type="application/ld+json")
        json_data = json.loads(all_news.string)
        return json_data['netWorth']['value']
    return None


def get_news():
    value_str = get_data(
        'https://www.forbes.com/profile/elon-musk/?list=rtb/&sh=29c7a18f7999'
    )
    if value_str:
        value = round(int(value_str) / 10 ** 9)
        title = [
            f'Шок! Состояние Илона Маска превысило ${value}B!',
            f'Собственный капитал Илона Маска уже ${value}B',
            f'${value}B собственный капитал владельца Теслы',
            f'Капитал основателя Tesla и SpaceX перешел оценку в ${value}B'
        ]

        text_news = [
            f'Генеральный директор Tesla - Илон Маск может позволить себе '
            f'{round(value/(100/73.8), 2)} дворца Путина',

            f'Forbes сообщает, что собственный капитал Илона Маска ${value}B',

            f'Рыночная оценка собственного капитала милиардера Илона Маска '
            f'уже ${value}B. Что будет, когда его машины будут летать?',

            f'По данным Forbes Илон Маск уже может купить себе '
            f'{round(value*(10**9)/142000)} машин Tesla'
        ]

        return {'title': random.choice(title),
                'text': random.choice(text_news)}
    return None
