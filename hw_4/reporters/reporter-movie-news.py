import feedparser
import html
from random import choice

name = "MoviesReporter"
version = "0.12"
depends = ['feedparser', 'html']
waiter = False


sentences = ['А вот и новости про кино...',
             'Запасаемся попкорном',
             'Самое главное о кино!',
             ]


def get_news():
    # Репортёр возвращает последнюю опубликованную новость на портале kinokadr

    url = 'feed://www.kinokadr.ru/export/rss.xml'
    news = feedparser.parse(url)

    last_one = news.entries[0]
    header = html.unescape(last_one['title'])
    link = html.unescape(last_one['links'][0]['href'])
    summary = html.unescape(last_one['summary'])

    return {'title': f'{choice(sentences)}  {header}',
            'text': f'А конкретнее: {summary} '
                    f'Полная новость по ссылке: {link}'}
