from urllib.request import urlopen
import json

name = "ValheimCounter"
version = "0.1"
depends = []
waiter = False


def get_news():
    url = "http://api.steampowered.com/ISteamUserStats" \
          "/GetNumberOfCurrentPlayers/v1/?appid=892970"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    value = data['response']['player_count']
    value = 1000 * (value // 1000)
    if value > 100000:
        return {'title': f'Valheim все еще популярна!',
                'text': f'В новую игру от малоизвестной компании '
                        f'Coffee Stain на данный момент играет около '
                        f'{value} игроков.'}
    else:
        return {'title': f'Valheim теряет популярность!',
                'text': f'В новую игру от малоизвестной компании '
                        f'Coffee Stain на данный момент играет всего '
                        f'лишь около {value} игроков.'}
