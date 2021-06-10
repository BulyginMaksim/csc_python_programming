from bs4 import BeautifulSoup
import requests
name = "RodoMaska"
version = "0.12"
depends = ['bs4']
waiter = True


def get_news():
    # ждем поступление в аптеку увлажняющей маски
    url = "https://apteka.ru/sankt-peterburg/product" \
          "/amplen-hyaluron-shot-uvlazhnyayushhaya-" \
          "dvuxstupenchataya-maska-s-gialuronom-5e425680f621e000014ba1ff/"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        is_available = soup.find('div', class_="ProductOffer__unavailable")
        if is_available is None:   # если None то поступила
            return {
                'title':
                f'Тот самый товар в наличии',

                'text':
                f'В Апатера.ру уже можно приобрести увлажняющую маску!'
            }
    return None


if __name__ == '__main__':
    get_news()
