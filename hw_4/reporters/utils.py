from urllib.request import urlopen
from urllib.error import URLError
import logging
from ReporterError import *


def get_content_from_url(url):
    try:
        url_open = urlopen(url)
    except URLError:
        logging.error("CurrencyCNY url error\n")
        raise ReporterError
    else:
        if url_open.getcode() != 200:
            logging.error(f"URL {url} return {url_open.getcode()} code!\n")
            raise ReporterError
        return url_open.read()
