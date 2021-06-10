from urllib.request import urlopen
import json

name = "RoboPetr"
version = "0.1"
depends = []
waiter = False


def get_news():
    import urllib.error
    import logging
    from socket import timeout

    url = "https://api.covid19api.com/summary"

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
        data = json.loads(data)
        return {
            'title': f'Ежедневная мировая статистика по коронавирусу.',
            'text':
                f'{data["Global"]["NewDeaths"]} - смертей за сегодня \n'
                f'{data["Global"]["TotalDeaths"]} - умерло всего \n'
                f'{data["Global"]["NewRecovered"]} - выздоровело за сегодня\n'
                f'{data["Global"]["TotalRecovered"]} - выздоровело всего \n'}
