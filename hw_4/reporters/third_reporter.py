from urllib.request import urlopen
import json

name = "RoboOleg"
version = "0.65"
depends = ['http.client']
waiter = False


def get_news():
    import http.client
    import logging

    try:
        connection = http.client.HTTPConnection('api.football-data.org')
    except http.client.HTTPException as e:
        logging.error("Data not retrieved, because: %s", e)
    except Exception as x:
        logging.error("Is there smth wrong: %s", x)
    else:
        logging.info("Access successful")

        f = open("token.txt", 'r')
        headers = {'X-Auth-Token': f.read()}
        f.close()
        connection.request('GET', '/v2/competitions/PL/matches/?matchday=25',
                           None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return {
            'title': f'{response["matches"][0]["utcDate"]} - день, когда '
                     f'вся футбольная общественность торжествовала',

            'text': f'Именно в этот день на одном поле сошлись 2 Английские '
                    f'команды: { response["matches"][0]["homeTeam"]["name"]} '
                    f'и { response["matches"][0]["awayTeam"]["name"]}. '
                    f'В данном случае наша редакция решила оставить новость '
                    f'без комментариев. Вы должны это посмотреть'}
