from urllib.request import urlopen
import json

name = "MarathonBet"
version = "0.0.1"
depends = ['bs4']
waiter = False


def get_news():
    from bs4 import BeautifulSoup
    url = 'https://www.marathonbet.ru/su/popular/Football+-+11'
    data = BeautifulSoup(urlopen(url), features='html.parser')
    # getting the teams of football games
    teams = data.find_all('div', {'class': 'today-member-name nowrap'})
    # getting the first game
    teams = [x.get_text().replace('\n', '')
             for i, x in enumerate(teams) if i < 2]
    team1, team2 = teams
    # getting coefs
    coefs = data.find_all(
        'span', {'class': 'selection-link active-selection'}
    )
    # getting coefs of the first game
    coefs = [x.get_text().replace('\n', '')
             for i, x in enumerate(coefs) if i < 3]
    win, draw, lose = coefs
    return f'Самый популярный ближайший футбольный матч: ' \
           f'{team1} против {team2}. ' \
           f'Коэффициенты:\n П1   XX   П2\n{win} {draw} {lose}\n' \
           f'Время делать ставку!'
