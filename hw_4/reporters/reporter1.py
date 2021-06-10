from bs4 import BeautifulSoup
import requests
import logging

name = "NataZen"
version = "0.1"
depends = ['bs4', 'requests']
waiter = False


def first_optional(it):
    try:
        return next(it)
    except StopIteration:
        logging.error(f"Nothing is found")
        return None


def get_news():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        filename='reporter1_log.txt',
        level=logging.ERROR
    )
    url = "https://www.isu.org/isu-news/news"
    html_response = requests.get(url)
    if html_response.url.endswith('error-404'):
        logging.error(f"Not found, 404")
    elif not html_response.ok:
        logging.error(f"Error code = {html_response.status_code}")
    else:
        soup = BeautifulSoup(html_response.text, "html.parser")
        return first_optional(link.p.get_text()
                              for link in soup.find_all('div',
                                                        class_='description'))
    return None
