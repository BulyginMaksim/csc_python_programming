# Репортер слдеит за курсом доллара и сообщает,
# когда доллар опустится ниже 65 рублей.

from urllib.request import urlopen
import json
import random


name = "Psycho-Level-USD"
version = "0.1"
depends = []
waiter = True


def get_news():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    value = data['Valute']['USD']['Value']
    if value < 65:
        return random.choice(['Неужели это наконец-то случилось!\n'
                              'Доллар опустился ниже 65 рублей и на '
                              f'данный момент торгуется по цене {value:.4}.',

                              'Доллар опустился ниже психологической отметки'
                              'в 65 рублей! Рубль продолжает укрепляться и '
                              f'на данный момент курс составляет {value:.4}.'])


if __name__ == "__main__":
    print(get_news())
