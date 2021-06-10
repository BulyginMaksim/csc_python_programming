"""
Репортер, который анализирует репозитории на гитхабе
и предоставляет статистику в виде новости, а именно,
если какой-нибудь репозиторий за один день набрал N звезд,
где N - достаточно большое (чтобы удивить) число, то он
попадает в новость.
"""
import json
import re
from datetime import datetime
from statistics import median
from urllib.parse import urlencode
from urllib.request import urlopen

name = "GitHubTop"
version = "0.1"
depends = []
waiter = True


def get_surprising(repos):
    median_deviation = 5
    stargazers_median = median([repo["stargazers_count"] for repo in repos])

    return list(filter(
        # we want to see repositories with an abnormally large stargazers count
        # therefore, we don't use the absolute values
        lambda repo:
            int(repo["stargazers_count"]) - \
            stargazers_median >= median_deviation,
        repos,
    ))


def get_news():
    current_date = datetime.now().date()

    # fetch all desired repos
    base_url = "https://api.github.com/search/repositories?"
    url_params = {
        "q": f"created:\">={current_date}\"",
        "sort": "stars",
        "order": "desc"
    }
    data = urlopen(base_url + urlencode(url_params)).read().decode("utf8")
    data = json.loads(data)

    surprising_repos = get_surprising(data["items"])

    if len(surprising_repos) > 0:
        text = f"""
            Удивительные вещи творятся в мире разработки. \
Например, всего за один день с момента создания \
репозиторий {surprising_repos[0]["name"]} \
(автор - {surprising_repos[0]["owner"]["login"]}) \
набрал аж {surprising_repos[0]["stargazers_count"]} звезд. \
А всего таких необычных репозиториев \
{len(surprising_repos)} - каждый набрал необычно много звезд.
        """.strip()
        re_normalize_ws = re.compile(r"\s{2,}")
        text = re_normalize_ws.sub(" ", text)

        return {
            "title": f"Известия Гитхаба - выпуск от {current_date}",
            "text": text,
        }
