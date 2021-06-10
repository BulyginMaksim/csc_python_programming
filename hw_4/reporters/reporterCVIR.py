# Репортер следит за темпами вакцинации в России.
# Сообщает информацию о количестве людей, получивших первый
# и второй компонент вакцины

import pandas as pd


name = "Covid-Vaccination-In-Russia-Reporter"
version = "0.1"
depends = ['pandas']
waiter = False


# Функция для правильного написания существительного вместе с числительным
def end(n):
    if 1 < n % 10 < 5:
        return "человека"
    else:
        return "человек"


def get_news():
    # Загрузка данных о количестве вакцинированных в стране
    url = 'https://raw.githubusercontent.com/owid/covid-19-data'\
          '/master/public/data/vaccinations/country_data/Russia.csv'
    data = pd.read_csv(url)
    # Загрузка данных об общем числе насиления страны
    url_p = 'https://raw.githubusercontent.com/owid/covid-19-data/'\
            'master/scripts/input/un/population_2020.csv'
    data_p = pd.read_csv(url_p)
    pop_in_rus = data_p.population.iloc[175]
    pv = int(data.people_vaccinated.iloc[-1])
    fpv = int(data.people_fully_vaccinated.iloc[-1])
    return f"Темпы вакцинации в России нарастают!\nУже {pv} {end(pv)} "\
           f"получили первый компонент вакцины,\n" \
           f"что составляет {pv / pop_in_rus * 100:.3}% " \
           f"от общего числа населения страны.\n" \
           f"Из них {fpv} получили второй компонент.\n" \
           f"Это {fpv / pop_in_rus * 100:.3}% населения.\n"\
           f"Напомним, что для отмены ограничений необходимо "\
           f"преодолеть планку в 60%."


if __name__ == "__main__":
    print(get_news())
