from urllib.request import urlopen
import json

name = "WitcherWaiter"
version = "0.1"
depends = []
waiter = True


def get_news():
    url = "https://store.steampowered.com/api/appdetails/?appids=292030"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    value = data['292030']['data']['price_overview']['discount_percent']
    if value > 0:
        return {'title': f'Ведьмак 3 сейчас по скидке, успей купить!',
                'text': f'Сейчас игра "Ведьмак 3: Дикая Охота" '
                        f'продается со скидкой {value} %.'}
    else:
        return None
