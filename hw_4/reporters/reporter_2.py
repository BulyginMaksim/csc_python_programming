from urllib.request import urlopen
import json
import random

name = "Covid reporter"
version = "0.1"
depends = []
waiter = False


def get_news():
    url = "https://api.covid19api.com/summary"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)

    total_cases = data['Global']['TotalConfirmed']
    new_cases = data['Global']['NewConfirmed']

    ret_vals = [
        {'title': 'Daily coronavirus spread report',
            'text': f'{new_cases} people got Covid-19 today!'},
        {'title': 'Daily coronavirus spread report',
         'text': f'Total number of infected with Covid-19 has increaed by '
                 f'{(100 * new_cases / (total_cases - new_cases)):.2f}% '
                 f'today!'},
        {'title': f'Total coronavirus cases as at {total_cases}!',
         'text': f'{total_cases} people got infected with Covid-19 '
                 f'from the beginning of pandemic!'}
    ]

    return random.choice(ret_vals)
