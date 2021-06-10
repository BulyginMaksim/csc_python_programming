from bs4 import BeautifulSoup
import requests
import datetime

name = "RodoBlackWidow"
version = "0.12"
depends = ['bs4']
waiter = True


def get_news():
    # ждем выхода фильма "Черная вдова"
    url = "https://en.wikipedia.org/wiki/Black_Widow_(2021_film)"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        date_str = soup.find('span', class_="bday dtstart published updated")
        lst_date = list(map(int, date_str.text.split('-')))
        date_premier = datetime.datetime(lst_date[0], lst_date[1], lst_date[2])
        date_now = datetime.datetime.now()
        if date_now >= date_premier:
            title = [f'Самый ожидаемый фильм Марвел уже вышел!',
                     f'Черная вдова возвращается!',
                     f'Наташа Романофф снова на экране!',
                     f'Скарлетт Йоханссон в главной роли шпионки \
уже можно увидеть на экранах!']
            text_news = [f'В кинотеатрах уже можно насладиться новым фильмов \
киновсселенной Marvel "Черная Вдова" с Скарлетт Йоханссон в главной роли.',
                         f'Несколько раз перенесенная премъера фильма \
режиссера Кейт Шортланд со Скарлетт Йоханссон в главной роли наконец-то \
состоялась!',
                         f'Долгожданная картина по комикасам Marvel вышла в \
кинотеатрах страны. Фильм "Черная Вдова" с Скарлетт Йоханссон обещает быть \
захватывающей!']
            return {'title': random.choice(title),
                    'text': random.choice(text_news)}
    return None
