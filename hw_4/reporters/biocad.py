from urllib.request import urlopen
import json

name = "BIOCAD"
version = "0.0.1"
depends = ['bs4', 'random', 're']
waiter = True


def get_news():
    from bs4 import BeautifulSoup
    import random
    import re
    url = 'https://career.biocad.ru/internships'
    data = BeautifulSoup(urlopen(url), features='html.parser')
    # getting the list of internships
    internships = data.find_all('div', {'class': 'icon-block'})
    internships = \
        [x.get_text().replace(' ', '').replace('\n', '')
            for x in internships]
    r = re.compile(r'IT(.*)')

    # немного костыль, но я не придумал, как сделать это красивее:(
    # getting the number of IT internships
    it = int(list(filter(r.search, internships))[0][3:-1])
    congratulations = [
        f'Ура! В BIOCAD появились IT стажировки! '
        f'Посмотрите, сколько их: {it}',

        f'Наконец-то! В BIOCAD появились IT стажировки! '
        f'Посмотрите, как много их: {it}',

        f'Дождались! Время подавать заявку на IT стажировку '
        f'в BIOCAD! Посмотрите, сколько их: {it}',

        f'Поторопитесь! Открыта подача на IT стажировки в BIOCAD! '
        f'Посмотрите, как много их: {it}'
    ]

    return None if it == 0 else random.choice(congratulations)
