import os
import sys
import logging
import concurrent.futures
from .models import News, Logs


logging.basicConfig(
    filename='miner.log',
    #           encoding='utf-8',
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG)

sys.path = ['../reporters'] + sys.path


def get_reporters():
    reporters = []
    reporters_files = os.listdir('../reporters')
    for r in reporters_files:
        print(r)
        if '__' not in r and r != 'Credentials.py':
            try:
                reporters.append(__import__(r[:-3]))
            except Exception as e:
                logging.error(f'{r} in reporters: {e}')
    return reporters


def get_data(reporters):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_name = {}
        for r in reporters:
            print(r)
            try:
                future_to_name[executor.submit(r.get_news)] = r.name
            except Exception as e:
                logging.error(f'{r} in reporters: {e}')
        data = {name: None for name in future_to_name.values()}
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                res = future.result()
                if res is not None:
                    data[name] = res
                else:
                    data[name] = f"{name} returned None"
            except Exception as e:
                data[name] = e
    return data


def push_inf_to_bd(data):
    for name in data:
        if type(data[name]) == dict and 'text' in data[name].keys():
            if not News.objects.filter(text=data[name]['text']).exists():
                news = News(reporter_name=name,
                            title=data[name]['title'],
                            text=data[name]['text'])
                news.save()
        else:
            log = Logs(reporter_name=name, log=data[name])
            log.save()


def mine():
    reporters = get_reporters()
    data = get_data(reporters)
    push_inf_to_bd(data)
