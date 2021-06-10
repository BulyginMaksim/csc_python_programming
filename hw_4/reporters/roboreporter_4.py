import random
from bs4 import BeautifulSoup
from datetime import date
from urllib.request import urlopen

name = "Pitchfork_fan_waiter"
version = "0.1"
depends = ['bs4', "datetime", "random", "urllib.request"]
waiter = True


def get_news():
    groups = ['Radiohead', 'Beck', 'TVoTR', 'Interpol', 'Portishead']
    dictionary = {
        "Title": [
            "Ты ждал, и этот день пришёл!",
            "Плачь, плачь, танцуй, танцуй!",
            "Пометь этот день в календаре крестиком."
        ],
        "Conclusion": [
            'наконец-то вошли в элитарные',
            'попали в',
            'удостоились чести быть добавленными в'
        ]
    }
    url = "https://pitchfork.com/best/"
    data = urlopen(url).read().decode('utf8')
    data_soup = BeautifulSoup(data, 'html.parser')

    best = data_soup.find_all("ul", {"class": "clearfix square-list"})
    songs = {song.li.contents[0]: song.h2.contents[0][1:-1]
             for song in best[1].find_all(
                 "div", {"class": "bnm-small track-small"})}

    # будем считать, что попадание хотя бы одной группы в список -
    # это новость, поэтому работаем до первого срабатывания
    for group in groups:
        if group in songs.keys():
            comp = songs[group]
            return {
                'title': f'Фанат {group}! '
                         f'{random.choice(dictionary["Title"])}',
                'text': f'Ровно {date.today().strftime("%d.%m.%y")} '
                        f'{group} c композицией {comp} '
                        f'{random.choice(dictionary["Conclusion"])} '
                        f'лучшие треки сайта Pitchfork. '}
    return {'title': "Не сегодня, фанат, не сегодня",
            'text': "В Pitchfork так просто не попасть"}
