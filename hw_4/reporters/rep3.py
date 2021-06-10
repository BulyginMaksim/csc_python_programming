from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from random import choice

name = "ArhivTracker"
version = "0.1"
depends = ["bs4"]
waiter = False


# Данный робожурналист находит последние публикации на сайте arhiv.org
def get_news():
    # ссылки на страницы с последними публикациями на arxiv.org
    new_urls = [
        ("Математика", "https://arxiv.org/list/math/new"),
        ("Физика", "https://arxiv.org/list/physics/new"),
        ("Компьютерные науки", "https://arxiv.org/list/cs/new"),
        ("Биология", "https://arxiv.org/list/q-bio/new"),
        ("Статистика", "https://arxiv.org/list/stat/new"),
        ("Экономика", "https://arxiv.org/list/econ/new"),
    ]
    theme, url = choice(new_urls)

    # получаем ссылку на первую публикацию
    text = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(text, 'html.parser')
    soup = soup.find('span', {'class': 'list-identifier'})
    article_url = urljoin(url, soup.find('a', {'title': 'Abstract'})['href'])

    # получаем название статьи
    text = urlopen(article_url).read().decode("utf-8")
    soup = BeautifulSoup(text, 'html.parser')
    title_soup = soup.find('h1', {'class': 'title mathjax'})
    title = title_soup.get_text().strip().removeprefix("Title:").strip()

    # получаем список авторов
    authors_soup = soup.find('div', {'class': 'authors'})
    authors = []
    for item in authors_soup.findAll('a'):
        authors.append(item.get_text())

    # получаем описание статьи
    quote_soup = soup.find('blockquote', {'class': 'abstract mathjax'})
    quote = quote_soup.get_text().strip().removeprefix('Abstract:').strip()

    titles = [
        f"Прорыв в области {theme}! "
        f"Группа ученых получила потрясающий результат!",

        f"Вышла новая статья в области {theme}. "
        f"В ней решена задача, которая было открытой на "
        f"протяжении многих лет",

        f"Ученые получили новый результат в области {theme}"
    ]
    texts = [
        '\n'.join([
            f"На сайте https://arxiv.org была опубликована "
            f"новая статья \"{title}\"",

            f"Авторы статьи {', '.join(authors)} утверждают, "
            f"что получили новый важный результат в этой области.",

            "Вот как они сами описывают свои результаты:",

            f'"{quote}"'
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
