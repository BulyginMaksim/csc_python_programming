from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import re

name = "ConsoleRobot"
version = "1.00"
depends = ["bs4"]
waiter = True

def get_news():
    try:
        url = "https://www.gamepark.ru/playstation5/console/IgrovayakonsolSonyPlayStation5/"
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
    except Exception as e:
        return logging.warning(f'Произошла ошибка при парсинге: {e}')

    try:
        text = soup.find_all("div", class_="box_price flex")[0].text
        price = re.findall("\d+", text.replace(" ", ""))[0]
        status = re.findall("Нет в наличии", text)
    except Exception as e:
        return logging.warning(f'Произошла ошибка при поиске цены: {e}')

    if not status:
        return {'title': f'PS5 появлиась в продаже!',
                'text': f'PS5 наконец-то появилась в розничной продаже по цене {price} руб.!'}

print(get_news())
