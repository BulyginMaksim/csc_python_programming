from urllib.request import urlopen
import json

name = "KFC"
version = "0.0.1"
depends = ['bs4']
waiter = False


def get_news():
    from bs4 import BeautifulSoup
    url = 'https://www.kfc.ru/coupons'
    data = BeautifulSoup(urlopen(url), features='html.parser')

    # description of all coupons
    description = data.find_all(
        'div',
        {'class':
         '_3POebZQSBG t-md c-description mt-16 pl-24 pr-24 condensed'}
    )
    description = [x.get_text().replace('\n', '') for x in description]

    # numbers of all coupons
    coupons = data.find_all('div', {'class': '_2pr76I4WPm'})
    coupons = [int(x.get_text()) for x in coupons]

    # initial prices of all coupons
    initial_price = data.find_all('span', {'class': 'fZklbU_aGI condensed'})
    initial_price = [int(x.get_text()) for x in initial_price]

    # final prices of all coupons
    final_price = data.find_all(
        'span', {'class': '_1trEHSCHMh condensed c-primary bold'}
    )
    final_price = [int(x.get_text()) for x in final_price]

    # profits of all coupons
    profits = [(initial - final) * 100 // initial
               for initial, final in zip(initial_price, final_price)]

    # getting index of the cheapest coupon
    the_cheapest_index = final_price.index(min(final_price))
    # getting index of the most profitable coupon
    the_most_profitable_index = profits.index(max(profits))

    return f'Самый дешевый купон: {coupons[the_cheapest_index]}. ' \
           f'Он содержит: {description[the_cheapest_index]} ' \
           f'и стоит всего лишь {final_price[the_cheapest_index]} рублей!\n' \
           f'Самый выгодный купон: {coupons[the_most_profitable_index]}. ' \
           f'Он содержит: {description[the_most_profitable_index]} ' \
           f'и стоит всего лишь {final_price[the_most_profitable_index]} ' \
           f'рублей! ' \
           f'Выгода {profits[the_most_profitable_index]}%!'
