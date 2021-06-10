import random
import math
import pandas as pd
"""
Этот репортер призван следить за числом страниц в русской вики.
Оно постоянно увеличивается!
"""
name = "RepoWiki"
version = "0.1"
depends = ["pandas"]
waiter = False


def art_case(n):
    if n % 100 in range(11, 19):
        return str(n) + ' статей'
    if n % 10 == 1:
        return str(n) + ' статья'
    if n % 10 in [2, 3, 4]:
        return str(n) + ' статьи'
    return str(n) + ' статей'


def get_news():
    url = "https://ru.wikipedia.org/wiki/" \
          "%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%" \
          "8F:%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0"
    data = pd.read_html(url)[0]
    num = int(data.loc[0, "Статистика по страницам.1"].replace(" ", ""))
    members = int(data.loc[7, "Статистика по страницам.1"].replace(" ", ""))
    mist = int(data.loc[4, "Статистика по страницам.1"].replace(" ", ""))
    news = [
        {'title': f'В википедии уже более {math.floor(num/10000) /100} млн. \
статей на русском языке!',
         'text': f'Cамая крупная энциклопедия интерната насчитывает \
на сегодняшний день почти'
                 f' {math.ceil(num/10000) /100} млн. статей, а также \
{round(members/1000000, 2)} млн. пользователей,'
                 f' активно правящих статьи на русском языке. \
Кстати, общее число правок уже'
                 f' превышает {math.floor(mist/1000000)} млн. \
Вы только вдумайтесь в эту цифру!'},
        {'title': f'Число страниц в русской википедии достигло отметки в \
{art_case(num)}.',
         'text': f'Cамая крупная энциклопедия интерната насчитывает \
на сегодняшний день почти'
                 f' {math.ceil(num/10000) /100} млн. статей, а также \
{round(members/1000000, 2)} млн. пользователей,'
                 f' активно редактирующих статьи на русском языке.'
                 f' Так держать! Науку в массы!'}
    ]
    return random.choice(news)


if __name__ == '__main__':
    res = get_news()
    print((res['title']).title())
    print((res['text']))
