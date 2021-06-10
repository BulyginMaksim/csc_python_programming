from urllib.request import urlopen
import re

name = "RoboVladimir"
version = "0.24"
depends = ['re']
waiter = True


def get_news():
    import urllib.error
    import logging
    from socket import timeout

    url = "https://iticapital.ru/shares/american-shares/dow-inc/"
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

        name = re.search(r'Акции (\w+)', data)
        value = re.search(r'(\d+),\d+', data)

        if name is None or value is None:
            logging.error("This page is different from what you expected")
            return {}

        if int(value.group(1)) > 10000:
            return {
                'title': 'Сенсация в мире химической промышленности!',
                'text':
                    f'Речь идет о немалоизвестной компании {name.group(1)}, '
                    f'которая сегодня обновила рекорд '
                    f'и стала самой дорогой химической компанией в новейшей '
                    f'истории человечества.'
                    f'дело в том, что один из немногих поверивших в эту '
                    f'молодую ценную бумагу в далеком '
                    f'2020 году был Эмиль Рахимов. Именно он сегодня, '
                    f'благодаря обновившейся цене на '
                    f'данную акцию(по сосстоянию на 24.03.2030 - '
                    f'{value.group()}) позволил себе '
                    f'купить сырок Б.Ю.Александров без скидки.'
            }
