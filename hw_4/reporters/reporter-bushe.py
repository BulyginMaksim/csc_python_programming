from datetime import datetime
import requests
from random import choice

name = "AlmondCroissantAssistant"
version = "0.12"
depends = ['requests']
waiter = True


sentences = ['О нет! В Буше больше нет миндального круассана...',
             'До свидания, миндальное блаженство :`(',
             'Как прощались с любимым круассаном Петербурга: краткая хроника',
             'У нас забрали главное - из Буше пропал миндальный круассан']

croissant_name = 'Круассан с миндальным кремом'


def get_news():
    # Это репортёр, который проверяет на сайте Буше возможность
    # приобрести миндальный круассан
    # В случае, если круассана нет, возвращается новость о том,
    # что круассан пропал
    url = 'https://bushe.ru/category/bdaefef6-bf33-7d4b-9b8f-f28058e129c3'
    date = datetime.today().strftime('%Y-%m-%d')
    content = requests.get(url).content.decode("utf-8")
    is_croissant_available = content.find(croissant_name)
    if is_croissant_available:
        return None
    return {'title': choice(sentences),
            'text': f'Сегодня: {date} миндальный круассан не был '
                    f'обнаружен в разделе с выпечкой :('}
