from urllib.request import urlopen
import re

name = "RoboIvan"
version = "0.12"
depends = ['re']
waiter = True


def get_news():
    import urllib.error
    import logging
    from socket import timeout

    url = "https://www.e-katalog.ru/prices/xiaomi-redmi-k40-pro-plus/"

    try:
        data = urlopen(url).read().decode('utf8')
    except urllib.error.HTTPError as e:
        logging.error("Data not retrieved, because: %s", e)
    except urllib.error.URLError as e:
        if isinstance(e.reason, timeout):
            logging.error("socket timed out - URL: %s", url)
        else:
            logging.error("Data not retrieved, because: %s", e.reason)
    except Exception as x:
        logging.error("Is there smth wrong: %s", x)
    else:
        logging.info("Access successful")

        data = urlopen(url).read().decode('utf8')
        value = re.search(r'Новинка ожидается', data)

        if value is not None:
            name = re.search(
                r'Цены на мобильный телефон (\w+)\s(\w+\s\w+\s\w+\s\w+)',
                data)
            cost = re.search(r'от (\w+\s\w+)', data)

            if name is None or cost is None:
                logging.error("This page is different from what you expected")
                return {}

            return {
                'title':
                'Самый ожидаемый флагман этого года наконец то выходит '
                'на рынок!',

                'text':
                f'И вновь хорошие новости от бренда {name.group(1)}. '
                f'Компания объявила старт продаж долгожданного смартфона '
                f'{name.group(2)}. Смартфон получит '
                f'новый процессор Snapdragon 888 и цена на них будет '
                f'начинаться с {cost.group(1)}. Поторопитесь!'}
