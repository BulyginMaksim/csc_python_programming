from urllib.request import urlopen
from random import choice
import json

name = "VaccinationTracker"
version = "0.1"
depends = ["json"]
waiter = False


# Данный робожурналист следит за темпами вакцинации в России и мире.
def get_news():
    vaccination_url = \
        "https://raw.githubusercontent.com/owid/covid-19-data" \
        "/master/public/data/vaccinations/vaccinations.json"
    data = json.loads(urlopen(vaccination_url).read().decode("utf-8"))
    total_vaccinated = 0
    russia_vaccinated = 0
    for country_item in data:
        country = country_item["country"]
        people_vaccinated = 0
        for item in country_item["data"]:
            lookup = ["people_fully_vaccinated", "people_vaccinated"]
            for key in lookup:
                if key in item:
                    people_vaccinated = item[key]
                    break
        total_vaccinated += people_vaccinated
        if country == "Russia":
            russia_vaccinated += people_vaccinated

    total_population = 7_854_575_277
    russia_population = 145_934_462

    titles = [
        f"Вакцинация идет огромными темпами",
        f"В России уже {russia_vaccinated / russia_population * 100:.2f}% "
        f"населения получили привику от коронавируса",

        f"Врач рассказал, когда следует ожидать окончания пандемии"
    ]
    texts = [
        '\n'.join([
            f"Главный врач страны предрек скорое окончания "
            f"пандемии в России. "
            f"По его словам, это получилось из-за стремительных "
            f"темпов вакцинации в России.",

            f"Эксперт отметил, что страны Евросоюза далеко отстают "
            f"от России в этом показателе.",

            f"По последним данным, в России привито уже "
            f"{russia_vaccinated / russia_population * 100:.2f}% населения "
            f"или {russia_vaccinated} человек.",

            f"В мире привито "
            f"{total_vaccinated / total_population * 100:.2f}% "
            f"населения или {total_vaccinated} человек.",
        ]),
    ]

    return {
        'title': choice(titles),
        'text': choice(texts),
    }


# data = get_news()
# if data is not None:
#     print(data['title'])
#     print()
#     print(data['text'])
# else:
#     print('None')
