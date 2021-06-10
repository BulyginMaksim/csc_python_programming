import pandas as pd
from datetime import date, timedelta

"""
Этот репортер призван следить за землятрясениями
на Курильских островах. т.е. сообщать случались ли они сегодня.
"""
name = "RepoKurilSeismic"
version = "0.1"
depends = ['pandas', 'lxml']
waiter = True


def hour_case(n):
    if n % 100 in range(11, 19):
        return str(n) + ' часов'
    if n % 10 == 1:
        return 'в первом часу утра'
    if n in [2, 3, 4]:
        return str(n) + ' часа утра'
    if n in [22, 23, 24]:
        return str(n) + ' часа'
    return str(n) + ' часов'


def get_data():
    url = "http://ds.iris.edu/seismon/eventlist/index.phtml?region=N_Pacific"
    df = pd.read_html(url)[0]
    today = date.today()

    df['DATE and TIME (UTC)'] = pd.to_datetime(df['DATE and TIME (UTC)'])
    df['DATE and TIME'] = df['DATE and TIME (UTC)'].apply(
        lambda s: s + timedelta(hours=3)
    )
    df["YEAR"] = df['DATE and TIME'].apply(lambda s: s.year)
    df["MONTH"] = df['DATE and TIME'].apply(lambda s: s.month)
    df["DAY"] = df['DATE and TIME'].apply(lambda s: s.day)
    df["HOUR"] = df['DATE and TIME'].apply(lambda s: s.hour)

    cond = (df["MONTH"] == today.month) & \
           (df["YEAR"] == today.year) & \
           (df["DAY"] == today.day) & \
           (df["LOCATION (Shows interactive map)"] == "KURIL ISLANDS")

    return df[cond]


def get_news():
    df = get_data()
    if len(df) == 0:
        return None
    df = df.sort_values(by=['MAG'], ascending=False)
    hour = df.iloc[0]["HOUR"]
    mag = df.iloc[0]["MAG"]
    # print(df[['DATE and TIME (UTC)', 'DATE and TIME']])

    news = [
        {'title': f'На Курильски островах произошло сильное землетрясение!',
         'text':
             f'Сегодня в {hour_case(hour)} по московскому времени \
на территории'
             f' Курильского бассеина произощло серьезное \
землятрясение.'
             f' По шкале Рихтера сила подземных толчков оценивается в \
{mag} пунктов. Следите за новостями!'},

        {'title': f'Небольшие землетрясения на Курилах.',
         'text': f'Сегодня жители и гости Курильски островов могли \
почувствовать подземные толчки.'
                 f' Всему виной очередное небольшое землетрясение.'
                 f' По данным сейсмологов его магнитуда не превышала \
{mag} пунктов.'
         }
    ]

    return news[0] if mag >= 7 else news[1]


if __name__ == '__main__':
    res = get_news()
    if res is not None:
        print((res['title']).title())
        print((res['text']))
