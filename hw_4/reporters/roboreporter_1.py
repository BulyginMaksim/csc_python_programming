import random
from bs4 import BeautifulSoup
from datetime import date
from urllib.request import urlopen

name = "Yandex_chart_fan"
version = "0.1"
depends = ['bs4', "datetime", "random", "urllib.request"]
waiter = False


def get_news():
    dictionary = {
        "Title": [
            "Ну что, любители музыки?",
            "Самые популярные треки здесь!",
            "Что же слушает Россия?"
        ],
        "Conclusion": [
            'Надеюсь, вы что-нибудь из этого знаете',
            'Поздравляем победителей!',
            "Что бы сказал об этом Лев Толстой..."
        ]
    }

    url = "https://music.yandex.ru/chart/"
    data = urlopen(url).read().decode('utf8')
    data_soup = BeautifulSoup(data, 'html.parser')

    chart_n = data_soup.find_all("div", {"class": "d-track__name"})
    chart_a = data_soup.find_all("div", {"class": "d-track__meta"})
    res = ''
    for i in range(5):
        authors = ', '.join(
            [i["title"] for i in
             chart_a[i].find_all("a", {"class": "deco-link deco-link_muted"})]
        )
        res += f"{i+1} место: {chart_n[i]['title']} - {authors}\r\n"

    return {'title': f'{random.choice(dictionary["Title"])} Топ-5 от '
                     f'Яндекс.Музыки на {date.today().strftime("%d.%m.%y")}',
            'text': f'{res}{random.choice(dictionary["Conclusion"])}'}
