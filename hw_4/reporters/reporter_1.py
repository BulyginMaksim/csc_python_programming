from urllib.request import urlopen
import random
from bs4 import BeautifulSoup

name = "PUBG reporter"
version = "0.1"
depends = ['beatifulsoup4']
waiter = False


def get_news():
    url = "https://store.steampowered.com" \
        "/stats/Steam-Game-and-Player-Statistics?l=t"
    data = urlopen(url).read().decode('utf8')
    bs = BeautifulSoup(data, features='html.parser')

    games_table = bs.body.div.find('div', class_='topgames_col').find(
        'table').findChildren(recursive=False)
    pubg_row = next(
        filter(lambda x:
               x.a is not None and 'PLAYER' in x.a.text, games_table))

    current_players = int(pubg_row.select('span')[0].text.replace(',', ''))
    todays_peak = int(pubg_row.select('span')[1].text.replace(',', ''))

    ret_vals = [
        {'title': 'PUBG\'s current online report',
         'text': f'PLAYERUNKNOWN\'S BATTLEGROUND now is at {current_players} '
                 f'players playing online.'},
        {'title': 'PUBG\'s daily peak players report',
         'text': f'Today PLAYERUNKNOWN\'S BATTLEGROUNDS had {todays_peak} '
                 f'players concurently.'}
    ]

    if current_players / todays_peak > 0.98:
        ret_vals.append(
            {'title': 'PUBG\'s online now is almost near today\'s maximum!',
             'text': f'PLAYERUNKNOWN\'S BATTLEGROUNDS now at '
                     f'{current_players} players online which '
                     f'is {(100 * current_players / todays_peak):.2f}% of '
                     f'daily maximum!'})
    if current_players / todays_peak < 0.7:
        ret_vals.append(
            {'title': 'PUBG\'s players are all asleep now',
             'text': f'PLAYERUNKNOWN\'S BATTLEGROUNDS now at '
                     f'{current_players} players online which is '
                     f'{(100 * current_players / todays_peak):.2f}% '
                     f'of daily maximum.'})

    return random.choice(ret_vals)
