# Репортер сообщает о последней публикации на портале https://arxiv.org
# в разделе Artificial Intelligence.

from urllib.request import urlopen
import feedparser
import random

name = "AIReporter"
version = "0.1"
depends = ['feedparser']
waiter = False


def get_news():
    # Сборка запроса
    base_url = "http://export.arxiv.org/api/query?"
    params = "search_query=cat:cs.AI&sortBy=submittedDate&"\
             "sortOrder=descending&max_results=1"
    url = base_url + params
    # Отправка запроса
    response = urlopen(url).read()
    data = feedparser.parse(response)
    # Извлечение необходимых данных, таких как авторы,
    # название статьи, summary, дата и время публикации
    entry = data.entries[0]
    aut = ", ".join([a['name'] for a in entry.authors])
    tit = entry.title
    pub, time = entry.published.replace("Z", "").split("T")
    su = entry.summary
    # Шаблоны для ответа
    patterns = [f"Strong AI is near! {aut} tell about {tit}.\n{su}\n{pub}",

                f"Yeah, science! {aut} presented wonderful opportunities AI "
                f"in article:\n{tit}.\n{su}\n{pub}",

                f"{tit}.\nWhat does it mean for AI technology?"
                f"Let's find out with {aut}.\n{su}\n{pub}"]
    return random.choice(patterns)


if __name__ == "__main__":
    print(get_news())
