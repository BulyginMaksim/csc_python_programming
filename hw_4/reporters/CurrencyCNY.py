import json
import random
import utils

name = "CNY"
version = "0.03"
depends = ['urllib', 'json']
waiter = True

threshold = 13
url = "https://www.cbr-xml-daily.ru/latest.js"


def get_two_rand(texts):
    indices = list(range(len(texts)))
    random.shuffle(indices)
    i, j = indices[:2]
    return texts[i], texts[j]


def produce_news(value):
    if value is None:
        return None
    text = [
        "Великий лидер Xi привел Китай к процвитанию, "
        "а бедный русский страдать от капитализм!\n",

        "Важный новость для русский друг, теперь великий Китай валюта вырасти,"
        "всем второй порция рис!",

        "Поддержка Русский товарищ и брат. Китайский валюта расти!",

        "Китайский рабочий показать большую сила Xi на рынок.Удар!",

        "Вступай Великий партия Китай, там вам дать кошкажена и два порция рис"
    ]  # it is popular meme, sorry
    first, second = get_two_rand(text)
    return {
        'title':
            f'Великий китайский юань теперь выше {threshold} русский рубль!',

        'text':
            f'{first}\n{second}\nВеликий китайский валюта теперь '
            f'равен {value} рубль!'
    }


def parse_data(data):
    data = json.loads(data)
    try:
        CNY_value = data['rates']['CNY']
    except KeyError:
        print(f"Couldn't found CNY info")
        return None
    else:
        if (type(CNY_value) is not float) or (not CNY_value > 0):
            print(f"Incorrect data on {url} in CNY field")
            return None
        value = 1 / CNY_value
        if value > threshold:
            return value


def get_news():
    data = utils.get_content_from_url(url).decode('utf8')
    value = parse_data(data)
    return produce_news(value)


if __name__ == '__main__':
    print(get_news())
