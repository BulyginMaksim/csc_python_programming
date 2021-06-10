# Репортер проверяет, обошел ли язык Python язык Java в рейтинге TIOBE.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import random


name = "PJReporter"
version = "0.1"
depends = ['BeautifulSoup']
waiter = True


# функция для нахождения языка программирования lang в
# строке s. В переменную perL запишется процентный показатель в
# рейтенге TIOBE для соответствующего языка.
def find_L(s, lang):
    st = s.find(lang)
    perL = ""
    for i in s[st + len(lang):]:
        perL += i
        if i == "%":
            break
    return st, perL


def get_news():
    url = "https://www.tiobe.com/tiobe-index/"
    data = urlopen(url).read()
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.table.tbody.text
    J, perJ = find_L(s, "Java")
    P, perP = find_L(s, "Python")
    details = "Посмотреть полный рейтинг можно здесь: "\
              "https://www.tiobe.com/tiobe-index/"
    # Если Python упоминается раньше, чем Java,
    # следовательно он выше в рейтинге.
    if P < J:
        return random.choice(["Python круче Java!\n"
                              "Согласно международному рейтингу TIOBE\n"
                              f"языки имеют показатели {perP} и {perJ} "
                              f"соответственно.\n{details}",

                              "Слизерин одолел Пуффендуй!\n"
                              "Международный рейтинг TIOBE оценил "
                              f"магические способности Python в {perP}, "
                              f"тогда как Java лишь в {perJ}.\n{details}"])


if __name__ == "__main__":
    print(get_news())
