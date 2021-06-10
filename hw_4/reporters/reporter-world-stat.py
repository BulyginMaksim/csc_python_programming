from urllib.request import urlopen
from random import choice
import json

name = "WorldStatReporter"
version = "0.12"
depends = []
waiter = True

threshold = 6000
headers = [f'Число записей о населении стран на портале worldpop.org '
           f'превысило {threshold}!',

           f'Вот это да! Больше {threshold} записей??? Ну дают...',

           'Классно: теперь на портале worldpop.org куча записей!']


def get_news():
    # Репортер проверяет, перевалило ли число записей о численности
    # населения разных стран на портале worldpop
    # за некоторое заданное значение

    url = 'https://www.worldpop.org/rest/data/pop/wpgp'
    with urlopen(url) as response:
        data = response.read()
        json_data = json.loads(data)
        number_of_records = len(json_data["data"])
    if number_of_records < threshold:
        return None
    return {'title': choice(headers),
            'text': f'Сейчас там {number_of_records} записей :)'}


print(get_news())
