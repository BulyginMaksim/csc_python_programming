import random
from bs4 import BeautifulSoup
from datetime import date
from urllib.request import urlopen

name = "Pitchfork_fan"
version = "0.1"
depends = ['bs4', "datetime", "random", "urllib.request"]
waiter = False


def get_news():
    dictionary = {
        "Title": [
            "Ну что, элита любителей музыки?",
            "Показалось, что всё вокруг недостаточно cool и совсем не edgy?",
            "Что же слушает группка элитарных снобов?"
        ],
        "Conclusion": [
            'Если что-то из этого знаете - гордитесь собой.',
            'Ну как, попали ваши любимчики??!?!!?',
            'Что бы сказал об этом вокальный коллектив "Сыновья России"...'
        ]
    }
    url = "https://pitchfork.com/best/"
    data = urlopen(url).read().decode('utf8')
    data_soup = BeautifulSoup(data, 'html.parser')

    best = data_soup.find_all("ul", {"class": "clearfix square-list"})
    songs = best[1].find_all("div", {"class": "bnm-small track-small"})
    res = ''
    for i in range(len(songs)):
        res += f"{i+1} музыкальная композиция: " \
               f"{songs[i].h2.contents[0][1:-1]} - " \
               f"{songs[i].li.contents[0]}\r\n"

    return {'title': f'{random.choice(dictionary["Title"])} Лучшие треки '
                     f'с сайта Pitchfork на '
                     f'{date.today().strftime("%d.%m.%y")}!',
            'text': f'{res}{random.choice(dictionary["Conclusion"])}'}
