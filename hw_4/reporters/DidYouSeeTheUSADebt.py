import math
import random
import pandas as pd
from urllib.request import urlopen

"""
Этот репортер призван неустанно всем напоминать,
что госдолг США постоянно увеличивается.
"""
name = "DidYouSeeTheUSADebt"
version = "0.1"
depends = ["pandas"]
waiter = False

dept = {
    0.8: ('практически в {} раза', 1),
    0.5: ('более чем в {} раза', 0.5),
    0.4: ('почти в {} раза', 0.5),
    0: ('в более чем {} раза', 0)
}


def my_round(x):
    frac = x - math.floor(x)
    s, addition = dept[frac]
    return s.format(math.floor(x) + addition)


def get_data():
    url = "https://fred.stlouisfed.org/data/GFDEBTN.txt"
    data = urlopen(url).read().decode('utf8')
    data = data.split("\n")[12:-1]
    data = map(str.split, data)
    df = pd.DataFrame(data, columns=["DATE", "VALUE"])
    df['DATE'] = pd.to_datetime(df['DATE'])

    df["YEAR"] = df['DATE'].apply(lambda s: s.year)
    df["MONTH"] = df['DATE'].apply(lambda s: s.month)
    df["DAY"] = df['DATE'].apply(lambda s: s.day)
    return df


def get_news():
    df = get_data()

    previous_value = int(df.iloc[-2]["VALUE"])
    last_value = int(df.iloc[-1]["VALUE"])
    year = df.iloc[-1]["YEAR"]
    last_year = int(df[(df.MONTH == 1) & (df.YEAR == year - 1)].VALUE)
    ten_years = int(df[(df.MONTH == 1) & (df.YEAR == year - 10)].VALUE)

    if last_value <= previous_value:
        title = f'Америка в глубокой пропасти: госдолг США составил \
${last_value // 1000000} трлн! \
Падение Америки: Госдолг США превысил отметку в ${last_value // 1000000} трлн.'
        sent = f' Аналитики подчитали, что за последние 10 лет долговая \
нагрузка Штатов увеличилась {my_round(last_value / ten_years)}. \
Эта беспрецидентная цифра позволяет судить о том, \
что США в скором времени столкнется с серьезными финансовыми трудностями.'
        return {'title': title, 'text': sent}

    titles = [
        f'Государственный долг США снова вырос: на этот раз сумма превысила \
${last_value // 1000000} трлн.',
        f'Когда падет финансовая пирамида: госдолг США вновь вырос \
дo ${last_value // 1000000} трлн.'
    ]

    proc = round((last_value - previous_value) / previous_value * 100)
    proc_year = round((last_value - last_year) / last_year * 100)
    phrases = [
        "Эксперты предполагают",
        "Аналитики уверяют",
        "Экономисты расчитывают"
    ]
    sent = f'В {year} году госдолг США вырос на \
${(last_value - previous_value) // 1000} млн. \
Эта беспрецидентная цифра позволяет судить о том, что США в скором времени \
столкнется с серьезными финансовыми \
{random.choice(["проблемами", "трудностями"])}, \
поскольку финансирование долга потребует от \
властей \
{random.choice(["повышения налогов", "уменьшения социальных выплат"])}. \
Особенно опасно выглядят темпы этого прироста. \
По последним опубликованным данным, объём бюджетного дефицита CША вырос \
на {proc}% по сравнению с прошлым кварталом, \
и на целых {proc_year}% по сравнению с показателями {year - 1} года. \
{random.choice(phrases)},\
что такой тренд будет наблюдаться и в будущем, если соответствующие меры \
не будут приняты американским правительством в ближайшее время.'

    res = {'title': random.choice(titles), 'text': sent}
    return res


if __name__ == '__main__':
    res = get_news()
    print((res['title']).title())
    print((res['text']))
