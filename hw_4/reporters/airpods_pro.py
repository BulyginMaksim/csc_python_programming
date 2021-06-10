from urllib.request import urlopen
import json

name = "AirPodsPro"
version = "0.0.1"
depends = ['bs4', 'random']
waiter = True


def get_news():
    from bs4 import BeautifulSoup
    import random
    DESIRED_PRICE = 20000
    url = \
        'https://www.apple.com/ru/shop/product/MWP22RU/A' \
        '/%D0%BD%D0%B0%D1%83%D1%88%D0%BD%D0%B8%D0%BA%D0%B8-airpods-pro'
    data = BeautifulSoup(urlopen(url), features='html.parser')

    # finding the price of airpods
    price = data.find('div', {'class': 'rf-pdp-currentprice'}).text
    # removing excess characters
    price = price.split('.', 1)[0]
    # still removing excess characters
    price = int(''.join((filter(str.isdigit, price))))
    congratulations = [
        f'Congratulations! It\'s time to buy AirPods Pro! '
        f'The current price is just {price}!',
        f'Good news! You have a chance to buy AirPods Pro '
        f'for the desired price! The current price is just {price}!',

        f'It\'s a high time to buy AirPods Pro! Hurry up and make an order! '
        f'The current price is just {price}!',

        f'Hohoho, X-day has come! Don\'t miss the chance to buy '
        f'AirPods Pro! The current price is just {price}!']

    return None if price > DESIRED_PRICE else random.choice(congratulations)
