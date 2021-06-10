from bs4 import BeautifulSoup
import requests
import logging
from collections import namedtuple


name = "NataZen"
version = "0.1"
depends = ['bs4', 'requests']
waiter = True


def parser_table_html(soup: BeautifulSoup) -> namedtuple:
    tables = soup.find_all('table')
    if len(tables) > 2:
        table = tables[1]
        Kinds = namedtuple('Kinds', ('total', 'short', 'free'))
        Details = namedtuple('Details', ('name', 'score', 'place'))
        for link in table.find_all('tr'):
            if '<th>' in str(link):
                column_names = [v for v in link.text.split('\n') if v]
            if 'Combined total' in str(link):
                total = [v for v in link.text.split('\n') if v]
            expected_href = '/wiki/Short_program_(figure_skating)'
            if [link for v in link.find_all('a')
                    if v.get('href') == expected_href]:
                short = [v for v in link.text.split('\n') if v]
            elif [link for v in link.find_all('a')
                    if v.get('href') == '/wiki/Free_skating']:
                free = [v for v in link.text.split('\n') if v]

        Kinds.total = Details(name=total[column_names.index('Skater')],
                              score=total[column_names.index('Score')],
                              place=total[column_names.index('Event')])
        Kinds.short = Details(name=short[column_names.index('Skater')],
                              score=short[column_names.index('Score')],
                              place=short[column_names.index('Event')])
        Kinds.free = Details(name=free[column_names.index('Skater')],
                             score=free[column_names.index('Score')],
                             place=free[column_names.index('Event')])

        return Kinds
    else:
        logging.error(f"Table is not found!")
        return None


def get_news_string(Kinds=None,
                    total_score=247.59,
                    short_score=85.45, free_score=166.62) -> str:
    news_string = ''
    if Kinds:
        if float(Kinds.short.score) > short_score:
            news_string += Kinds.short.name + \
                ' sets a record in the short program of ' + \
                Kinds.short.score + ' at ' + \
                Kinds.short.place + '!\n'
        if float(Kinds.free.score) > free_score:
            news_string += Kinds.free.name + \
                ' sets a record in the free program of ' + \
                Kinds.free.score + ' at ' + Kinds.free.place + '!\n'
        if float(Kinds.total.score) > total_score:
            news_string += Kinds.total.name + \
                ' sets a record in the total program of ' + \
                Kinds.total.score + ' at ' + \
                Kinds.total.place + '!\n'
    return news_string


def get_news():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        filename='reporter2_log.txt',
        level=logging.ERROR
    )
    url = "https://en.wikipedia.org/wiki" \
        "/List_of_highest_scores_in_figure_skating"
    html_response = requests.get(url)
    if html_response.url.endswith('error-404'):
        logging.error(f"Not found, 404")
    elif not html_response.ok:
        logging.error(f"Error code = {html_response.status_code}")
    else:
        soup = BeautifulSoup(html_response.text, "html.parser")
        Kinds = parser_table_html(soup)
        news_string = get_news_string(Kinds)
        if news_string:
            return news_string
    return None
