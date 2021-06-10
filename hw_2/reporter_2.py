from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import re
import json

name = "RofloRobot"
version = "1.00"
depends = ["bs4"]
waiter = True

def get_news():
    try:
        url_world = "https://worldpopulationreview.com/"
        url_video = "https://www.googleapis.com/youtube/v3/thereshouldbesomekey/"
        data_video = urlopen(url_video)
        html_world = urlopen(url_world)
        soup_world = BeautifulSoup(html_world, features="html.parser")
        text_world = soup_world.find_all("div", class_="section-container clearfix")
        data_video = json.loads(data_video.read().decode('utf8'))
    except Exception as e:
        return logging.warning(f'Произошла ошибка при парсинге: {e}')

    try:
        world_population = int(re.findall("\d+", text_world[2].text.replace(",", ""))[1])
        view_count = int(data_video["items"][0]["statistics"]["viewCount"])
    except Exception as e:
        return logging.warning(f'Произошла ошибка при поиске значения населения/количества просмотров: {e}')

    if view_count > world_population:
        return {'title': f'{name} сообщает экстренные рофлоновости!',
                'text': f'Количество просмотров под клипом Despacito ({view_count} просмотров) наконец-то перевалило '
                        f'население земли (приблизительно {world_population} человек в мире данный момент)!'}

print(get_news())