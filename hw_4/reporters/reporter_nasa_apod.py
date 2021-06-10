from urllib.request import urlopen
from datetime import datetime
from random import choice
import json

name = "SpaceReporter"
version = "0.12"
depends = []
waiter = False

key = '(ключ)'
adjectives = ['невероятное', 'поражающее воображение',
              'впечатляющее', 'неожиданное', 'классное',
              'космическое (pun intended)', 'красочное']

image = 'image'
pic = 'изображение'
video = 'видео'


def get_news():
    # Этот репортер возвращает название и ссылку на сегодняшнее
    # изображение или видео, опубликованное NASA
    date = datetime.today().strftime('%Y-%m-%d')
    url = f'https://api.nasa.gov/planetary/apod?date={date}&api_key={key}'
    with urlopen(url) as response:
        data = response.read()
        json_data = json.loads(data)
        media_type = json_data["media_type"]
        title = json_data["title"]
        url = json_data["url"]
    return {'title': f'Сегодня ({date}) NASA опубликовали '
                     f'{choice(adjectives)} '
                     f'{pic if media_type == image else video}!',
            'text': f'Название: {title}, а посмотреть можно '
                    f'по ссылке: {url}'}
