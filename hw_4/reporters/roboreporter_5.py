import random
from bs4 import BeautifulSoup
from datetime import date
from urllib.request import urlopen

name = "Spotify_fan_waiter"
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
    url = "https://spotifycharts.com/regional/"

    hdr = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
           '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',

           'Accept':
           'text/html,application/xhtml+xml,application/xml;'
           'q=0.9,*/*;q=0.8',

           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib.request.Request(url, headers=hdr)
    data = urlopen(req).read().decode('utf8')
    data_soup = BeautifulSoup(data, 'html.parser')

    songs = {song.span.contents[0][3:]: song.strong.contents[0]
             for song in data_soup.find_all(
                 "td", {"class": "chart-table-track"})}

    for group in groups:
        if group in songs.keys():
            comp = songs[group]
            return {
                'title': f'Фанат {group}! '
                         f'{random.choice(dictionary["Title"])}',
                'text': f'Ровно {date.today().strftime("%d.%m.%y")} '
                        f'{group} c композицией {comp} '
                        f'{random.choice(dictionary["Conclusion"])} '
                        f'топ-10 Spotify.'
            }
    return {'title': "Не сегодня, фанат, не сегодня",
            'text': "В топ-10 Spotify так просто не попасть"}
