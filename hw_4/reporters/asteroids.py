"""
Репортер, который берет информацию о близких к Земле
астероидах из API Near Earth Object Web Service.
Новость содержит некоторую статистику по астероидам -
их число, сколько из них опасных и границы их размеров.

Немного комментариев дальше в коде.
"""

import json
import locale
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import urlopen

name = "Asteroids"
version = "0.1"
depends = []
waiter = False


@dataclass
class Asteroid:
    asteroid_id: int
    asteroid_name: str
    estimated_diameter_min: float
    estimated_diameter_max: float
    is_potentially_hazardous: bool


def fetch_asteroids(start_date=None, end_date=None):
    if start_date is None:
        start_date = datetime.now().date()
    if end_date is None:
        end_date = datetime.now().date()

    if start_date > end_date:
        raise ValueError("start date must be before end date")

    if (end_date - start_date).days > 7:
        raise ValueError("date window must be no more that 7 days")

    # fetch the data from the api
    base_url = "http://www.neowsapp.com/rest/v1/feed?"
    url_params = {
        "start_date": start_date,
        "end_date": end_date,
        "detailed": False,
        "api_key": "DEMO_KEY"
    }
    data = urlopen(base_url + urlencode(url_params)).read().decode("utf8")
    data = json.loads(data)

    # get all asteroids from the json data
    asteroids = []
    for i in range((end_date - start_date).days + 1):
        current_day_str = str(start_date + timedelta(days=i))
        near_earth_objects = data["near_earth_objects"][current_day_str]
        for obj in near_earth_objects:
            asteroid_id = obj["id"]
            asteroid_name = obj["name"]
            estimated_diameter_min = \
                obj["estimated_diameter"]["meters"]["estimated_diameter_min"]
            estimated_diameter_max = \
                obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
            is_potentially_hazardous = obj["is_potentially_hazardous_asteroid"]

            asteroid = Asteroid(
                asteroid_id,
                asteroid_name,
                estimated_diameter_min,
                estimated_diameter_max,
                is_potentially_hazardous,
            )
            asteroid.estimated_diameter_min = \
                round(asteroid.estimated_diameter_min, 2)
            asteroid.estimated_diameter_max = \
                round(asteroid.estimated_diameter_max, 2)

            asteroids.append(asteroid)

    return asteroids


def get_news():
    locale.setlocale(locale.LC_ALL, "ru_RU.utf8")

    today_str = str(datetime.now().date())
    asteroids = fetch_asteroids()

    # find info about hazardous asteroids
    hazardous_asteroids = \
        list(filter(lambda a: a.is_potentially_hazardous, asteroids))
    hazardous_asteroids_names = \
        [a.asteroid_name for a in hazardous_asteroids] + ["aaa"]
    hazardous_asteroids_text = "Опасных среди них нет."
    if len(hazardous_asteroids) == 1:
        hazardous_asteroids_text = \
            f"Среди них есть и опасный - " \
            f"это астероид {hazardous_asteroids_names[0]}."
    elif len(hazardous_asteroids) > 1:
        hazardous_asteroids_text = \
            f"Среди них есть и опасные - " \
            f"это астероиды {', '.join(hazardous_asteroids_names)}."

    # get some statistics about asteroids
    min_est_diameter_max_asteroid = \
        min(asteroids, key=lambda a: a.estimated_diameter_max)
    max_est_diameter_max_asteroid = \
        max(asteroids, key=lambda a: a.estimated_diameter_max)

    # build a text
    title = \
        f"Сегодня рядом с Землёй пролетят {len(asteroids)} " \
        f"астероидов. Подробности внутри."
    text = "Астероидов не будет - можно спать спокойно :)"
    if len(asteroids) > 0:
        text = f"""
            Источники из NASA сообщают, что сегодня, {today_str}, \
рядом с Землёй пролетят {len(asteroids)} астероидов.
            {hazardous_asteroids_text}
            Кроме того, аналитики изучили данные и определили размеры \
этих {len(asteroids)} астероидов.
            Так как астероиды имеют разные диаметры (они не сферические), \
то мы расскажем про наибольшие.
            Астероид {max_est_diameter_max_asteroid.asteroid_name} имеет \
самый большой диаметр, равный
            {max_est_diameter_max_asteroid.estimated_diameter_max} метров, \
а астероид
            {min_est_diameter_max_asteroid.asteroid_name} имеет наименьший \
диаметр - {min_est_diameter_max_asteroid.estimated_diameter_max} метров.
        """.strip()
        re_normalize_ws = re.compile(r"\s{2,}")
        text = re_normalize_ws.sub(" ", text)

    return {"title": title, "text": text}
