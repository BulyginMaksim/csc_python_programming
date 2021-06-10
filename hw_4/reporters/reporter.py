from urllib.request import urlopen
import json
from datetime import date
from random import choice

name = "CovidDay"
version = "0.12"
depends = ['numpy', 'pandas', 'datetime', 'random']
waiter = False

# this reporter tells us whether this day is better than the previous
# week in terms of new covid cases


def get_news():
    def dat_conv(dt):  # converts data to the usual Python format
        listt = dt.split("-")
        return date(int(listt[0]), int(listt[1]), int(listt[2]))

    url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    avg_covid = 0
    today_covid = 0
    while (avg_covid == 0):
        avg_covid = 0
        country = choice(list(data.keys()))  # country where we choose
        leng = len(data[country]['data'])
        today_covid = data[country]['data'][leng - 1]['new_cases']
        for i in range(leng - 8, leng - 1):
            avg_covid += data[country]['data'][i]['new_cases']
        namee = data[country]['location']

    if today_covid > 1.2 * avg_covid / 7:
        return {'title': f'Covid-tough day in {namee}!',
                'text': f'''This day was not very lucky for {namee}.
They have {today_covid} new cases, which is \
{round((today_covid/avg_covid*7)*100)-100}% above \
            the weekly average. \
The government is discussing new restrictions \
            in order to prevent catastrophe.'''}
    elif (today_covid < 0.8 * avg_covid / 7):
        return {'title': f'Lucky day in {namee}!',
                'text': f'''Today was quite nice for {namee}. \
They have a major decrease in new cases ({today_covid} today) \
, which is {-round((today_covid/avg_covid*7)*100)+100}% below \
the weekly average.'''}
    else:
        return {'title': f'In {namee} the Covid situation is stable',
                'text': f'''Another usual day of the Covid-19 pandemic \
passed in {namee}. \
They have {today_covid} cases, which is quite close to \
the weekly average.'''}
