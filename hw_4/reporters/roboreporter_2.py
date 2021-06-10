import random
from datetime import date
from urllib.request import urlopen

name = "Spotify_chart_fan"
version = "0.1"
depends = ['bs4', "datetime", "random", "urllib.request"]
waiter = False


def get_news():
    dictionary = {
        "Title": [
            "Ну что, настоящие любители музыки?",
            "Самые популярные мировые треки здесь!",
            "Что же слушает весь мир?"
        ],
        "Conclusion": [
            'Если что-то из этого не знаете - бегом слушать!',
            'Ну как, попали ваши любимчики?',
            "Что бы сказал об этом Теккерей..."
        ]
    }
    url = "https://spotifycharts.com/regional/"

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                         '(KHTML, like Gecko) Chrome/23.0.1271.64 '
                         'Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;'
                     'q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib.request.Request(url, headers=hdr)
    data = urlopen(req).read().decode('utf8')
    data_soup = BeautifulSoup(data, 'html.parser')

    charts = data_soup.find_all("td", {"class": "chart-table-track"})
    res = ''
    for i in range(5):
        res += f"{i+1} место: {charts[i].strong.contents[0]} - " \
               f"{charts[i].span.contents[0][3:]}\r\n"

    return {'title': f'{random.choice(dictionary["Title"])} '
                     f'Топ-5 от Spotify на '
                     f'{date.today().strftime("%d.%m.%y")}',
            'text': f'{res}{random.choice(dictionary["Conclusion"])}'}
