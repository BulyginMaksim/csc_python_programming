from urllib.request import urlopen
import logging
from bs4 import BeautifulSoup
import re

name = "CryptoRobot"
version = "1.00"
depends = ["bs4"]
waiter = False

def get_opt_message(btc_value, eth_value):
    if float(btc_value.replace(",", ".")) > 58000 and float(eth_value.replace(",", ".")) > 1900:
        return f" {name} соболезнует тем, кто задумывался приобрести видеокарту :("
    else:
        return ""

def get_crypto(crypto):
    crypto_value, crypto_dif = re.findall(r".+", crypto.text.replace(" ", ""))[1:]
    if crypto_dif[0] == "+":
        return crypto_value, f"вырос на {crypto_dif[1:]}%"
    else:
        return crypto_value, f"упал на {crypto_dif[1:]}%"

def get_news():
    try:
        url = "https://www.rbc.ru/crypto/"
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.find_all("div", class_="currencies__col")
    except Exception as e:
        return logging.warning(f'Произошла ошибка при парсинге: {e}')

    try:
        btc_value, btc_dif = get_crypto(text[2])
        eth_value, eth_dif = get_crypto(text[3])
        optional_message = get_opt_message(btc_value, eth_value)
    except Exception as e:
        return logging.warning(f'Произошла ошибка поиске значений курсов криптовалюты: {e}')

    return {'title': f'Курс биткоина составляет {btc_value}$, а эфириума {eth_value}$!',
            'text': f'За последние 24 часа биткоин {btc_dif} и стал стоить {btc_value}$,'
                    f'а эфириум {eth_dif} и стал стоить {eth_value}$!{optional_message}'}

print(get_news())