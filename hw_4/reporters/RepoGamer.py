import random
from urllib.request import urlopen
"""
Этот репортер призван следить за распродажами в стиме на определенные игры.
"""
name = "RepoGamer"
version = "0.1"
depends = []
waiter = True
urls = {
    "Red Dead Redemption 2":
    "https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/",

    "The Witcher 3: Wild Hunt":
    "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",

    "Borderlands 3":
    "https://store.steampowered.com/app/397540/Borderlands_3/"
}


def rub_case(n):
    if n % 100 in range(11, 19):
        return str(n) + ' рублей'
    if n % 10 == 1:
        return str(n) + ' рубль'
    if n % 10 in [2, 3, 4]:
        return str(n) + ' рубля'
    return str(n) + ' рублей'


def get_data():
    games = list(urls.keys())
    random.shuffle(games)
    pattern = 'class="discount_block game_purchase_discount" ' \
              'data-price-final="'

    for game in games:
        data = urlopen(urls[game]).read().decode('utf8')
        pos = data.find(pattern)
        if pos != -1:
            break
    if pos == -1:
        # нет распродаж ;(
        return None, None, None, None, None

    price = ''
    for s in data[pos + len(pattern):]:
        if not s.isdigit():
            break
        price += s
    price = int(price[:-2])
    disc = ''
    disc_pos = data.find('%', pos + len(pattern))
    for s in data[disc_pos - 1:pos:-1]:
        if not s.isdigit():
            break
        disc += s
    disc = disc[::-1]
    pos = data.find("Offer ends ")
    date = data[pos + len("Offer ends "): data.find("<", pos)]
    day, month = date.split()[0], date.split()[1]

    return price, disc, game, day, month


def get_news():
    price, disc, game, day, month = get_data()
    if game is None:
        return None

    d = {"January": "января", "February": "февраля",
         "March": "марта", "April": "апреля", "May": "мая",
         "June": "июня", "July": "мюля", "August": "августа",
         "September": "сентября", "October": "октября", "November": "ноября",
         "December": "декабря"}
    news = [
        {'title': f'Успейте приобрести {game} cо скидкой {disc}%!',
         'text': f'Предложение действует до {day} \
{d[month]} в магазине STEAM.'},
        {'title': f'Культовая игра {game} по скидке {disc}% в STEAM!',
         'text': f'В магазине STEAM в рамках распродажи можно \
приобрести всеми любимую'
                 f' {game} теперь всего за {rub_case(price)}.'}
    ]
    return random.choice(news)


if __name__ == '__main__':
    res = get_news()
    if res is not None:
        print((res['title']).title())
        print((res['text']))
