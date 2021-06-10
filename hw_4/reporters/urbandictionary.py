"""
Репортер, который собирает небольшую статистику
по словам с Urban Dictionary, и презентует в новости.
Например, слово месяца (с наибольшим числом лайков),
самое длинное слово года или самое задизлайканное.

Остальные моменты в комментариях в коде.
"""

import calendar
import itertools
import random
import re
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup

name = "WordOfTheMonth"
version = "0.1"
depends = ["bs4"]
waiter = False


def get_page_url(page_number):
    if page_number < 1:
        raise ValueError(f"incorrect page number: {page_number}, must be >= 1")

    base_url = "https://www.urbandictionary.com/"
    if page_number == 1:
        return base_url
    else:
        return f"{base_url}?page={page_number}"


def definition_to_object(definition):
    # "word of the day" text
    wotd_str = definition.find(class_="ribbon").text

    # extract month and day strings
    month, day = wotd_str.split()[:2]
    month = month.upper()

    # extract the word itself
    word = definition.find(class_="word").text

    # extract likes and dislikes count
    thumbs_counts = definition.find(class_="thumbs").find_all(class_="count")
    likes = int(thumbs_counts[0].text)
    dislikes = int(thumbs_counts[1].text)

    return {"month": month, "day": day, "word": word,
            "likes": likes, "dislikes": dislikes}


def words_of_month(month=None):
    # take the current month if none is specified
    if month is None:
        month = datetime.now().strftime("%h").upper()

    # go through the pages and get all the words we need
    words = []
    current_page = 1
    stop = False
    while not stop:
        current_url = get_page_url(current_page)
        data = urlopen(current_url).read().decode("utf8")

        soup = BeautifulSoup(data, "html.parser")
        content = soup.find(id="content")
        definitions = content.find_all(class_="def-panel")

        for word in map(definition_to_object, definitions):
            if word["month"] == month:
                words.append(word)
            elif len(words) > 0:
                stop = True
                break

        current_page += 1

    return words


def get_news():
    current_month_number = int(datetime.now().strftime("%m"))
    current_year_number = int(datetime.now().strftime("%y"))

    # find the word of the current month with the maximum likes
    current_month_words = words_of_month()
    max_likes_word = max(current_month_words, key=lambda w: w["likes"])

    # come up with another fact (within the year)
    months_of_year = map(
        lambda n: calendar.month_abbr[n].upper(),
        range(1, current_month_number + 1),
    )
    words_of_year = itertools.chain.from_iterable(
        map(words_of_month, months_of_year))
    fact = random.choice(["longest", "shortest", "max_likes", "max_dislikes"])
    fact_text = "интересного факта не нашлось :("
    if True or fact == "longest":
        longest_word = max(words_of_year, key=lambda w: len(w["word"]))
        fact_text = f"самым длинным словом оказалось {longest_word['word']}"
    elif fact == "shortest":
        shortest_word = min(words_of_year, key=lambda w: len(w["word"]))
        fact_text = f"самым коротким словом оказалось {shortest_word['word']}"
    elif fact == "max_likes":
        year_max_likes_word = max(words_of_year, key=lambda w: w["likes"])
        fact_text = \
            f"словом с наибольшим числом лайков оказалось " \
            f"{year_max_likes_word['word']}"
    elif fact == "max_dislikes":
        year_max_dislikes_word = max(words_of_year,
                                     key=lambda w: w["dislikes"])
        fact_text = f"словом с наибольшим числом дизлайков " \
                    f"оказалось {year_max_dislikes_word['word']}"

    # build a text
    title = f"Слово месяца по версии Urban Dictionary - " \
            f"{max_likes_word['word']} ({max_likes_word['likes']} лайков)"
    text = f"""
В {current_month_number}-м месяце этого года ведущие аналитики \
портала Urban Dictionary провели анализ пользовательских предпочтений \
и определили слово месяца. Таким словом оказалось {max_likes_word['word']} \
- оно набрало аж {max_likes_word['likes']} лайков. \
Удивительно, не правда ли? А ещё один интересный факт про \
{current_year_number}-й год - {fact_text}.
    """.strip()
    re_normalize_ws = re.compile(r"\s{2,}")
    text = re_normalize_ws.sub(" ", text)

    return {"title": title, "text": text}
