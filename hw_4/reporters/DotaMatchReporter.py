import logging
import bs4
import random

import utils

name = "DotaMatchReporter"
version = "0.01"
depends = ['bs4']
waiter = False

url = "https://liquipedia.net/dota2/Main_Page"


class MatchInfo:

    def __init__(self, team1_file, team2_file, res1, res2):
        self.team1 = get_team_name(team1_file)
        self.team2 = get_team_name(team2_file)
        self.res1 = int(res1)
        self.res2 = int(res2)


def get_team_name(team_div):
    soup = bs4.BeautifulSoup(str(team_div), "lxml")
    ref = soup.find("a", {"class": "new"})
    return ref.contents[0]


def get_last_match_info(table):
    div_soup = bs4.BeautifulSoup(str(table), "lxml")
    team1_file, team2_file = (div_soup.find("td", {"class": class_})
                              for class_ in ("team-left", "team-right"))
    res1, _, res2 = filter(
        lambda x: x.isdigit() or x == ':',
        div_soup.find("td", {"class": "versus"}).text
    )
    return MatchInfo(team1_file, team2_file, res1, res2)


def generate_news(match):
    if match is None:
        return None
    result_title = {
        (1, 0): [
            f"{match.team1} выиграла у {match.team2} cо счётом 1:0!",
            f"{match.team1} одержала небольшую победу над {match.team2}, \
победив в 1 карте!",
            f"{match.team1} и {match.team2} сыграли BO1 со счётом 1:0!"
        ],
        (2, 0): [
            f"{match.team1} без шансов одержала победу над {match.team2} \
cо счётом 2:0!",
            f"{match.team2} не смогла урвать ни одной карты у {match.team1}!"
        ],
        (3, 0): [
            f"{match.team1} вынесла {match.team2} cо счётом 2:0!",
            f"{match.team2} не смогла урвать ни одной карты у \
{match.team1}!",
            f"{match.team1} устроила похорны {match.team2} в финале, \
со счётом 3:0!"
        ],
        (0, 1): [
            f"{match.team1} проиграла {match.team2} cо счётом 0:1!",
            f"{match.team1} уступила одну карту {match.team2}!",
            f"{match.team1} и {match.team2} сыграли BO1 со счётом 0:1!"
        ],
        (0, 2): [
            f"{match.team1} без шансов проиграла {match.team2} cо счётом 0:2!",
            f"{match.team1} не смогла урвать ни одной карты у {match.team2}!"
        ],
        (0, 3): [
            f"{match.team1} отлетла от {match.team2} cо счётом 0:3!",
            f"{match.team1} не смогла урвать ни одной карты у {match.team2}!",
            f"{match.team2} устроила похорны {match.team1} в финале, \
со счётом 3:0!"
        ],
        (1, 1): [
            f"Cкучная ничья между {match.team1} и {match.team2}"
        ]
    }
    title_com = [
        f"{match.team1} сыграла с {match.team2} со счётом \
{match.res1}:{match.res2}"
    ]
    final_epic = [
        f"Эпичный финал между {match.team1} и {match.team2} состоявший из 5 "
        f"карт закочился победой \
{match.team1 if match.res1 > match.res2 else match.team2}!!!"
    ]
    match_epic = [
        f"Жесткое противостояние между {match.team1} и {match.team2} "
        f"состоявший в BO3 закочился победой \
{match.team1 if match.res1 > match.res2 else match.team2}!!!"
    ]
    title = result_title.get((match.res1, match.res2), []) + title_com
    if match.res1 + match.res2 == 5:
        title += final_epic
    if (match.res1 == 2 and match.res2 == 1) \
            or (match.res1 == 1 and match.res2 == 2):
        title += match_epic
    text = f"""Недавно завершился матч по Dota 2, где сошлись
две команды {match.team1} и {match.team2}.
Игра закончилась со счётом {match.res1}:{match.res2}"""

    return {'title': {random.choice(title)},
            'text': text}


def parse_data(data):
    soup = bs4.BeautifulSoup(data, "lxml")  # html parse
    div = soup.find("div", {"data-toggle-area-content": "3"})
    if len(div.contents) < 2:
        logging.error("Can't find last match")
        return None
    return get_last_match_info(div.contents[1])


def get_news():
    data = utils.get_content_from_url(url)
    match_info = parse_data(data)
    return generate_news(match_info)
