from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from random import choice

name = "PythonUpdate"
version = "0.1"
depends = ["bs4"]
waiter = True


# Данный робожурналист ждет, когда выйдет новая версия языка Python
# Считается, что текущая версия это 3.9.2
def get_news():
    last_version = "3.9.2"
    url = "https://www.python.org/downloads/"

    text = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(text, 'html.parser')
    soup = soup.find('div', {'class': 'download-unknown'})

    download_url = urljoin(url, soup.p.a["href"])

    text_button = soup.p.a.get_text()
    new_version = text_button.removeprefix("Download Python").strip()

    if new_version != last_version:
        titles = [
            f"Вышла новая версия Python {new_version}",
            f"Стала доступна новая версия языка программирования Python",
            f"Уже {new_version}! Новые версии Python выходят все чаще!"
        ]
        texts = [
            f"На официальном сайте https://www.python.org/ стала доступна "
            f"для скачивания новая версия Python {new_version}.\nЕе можно "
            f"скачать по этой ссылке: {download_url}",
        ]
        return {
            'title': choice(titles),
            'text': choice(texts)
        }
    else:
        return None


# data = get_news()
# if data is not None:
#     print(data['title'])
#     print()
#     print(data['text'])
# else:
#     print('None')
