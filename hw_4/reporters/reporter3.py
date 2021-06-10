from urllib.request import urlopen
import json
import ssl
name = "NataZen"
version = "0.1"
depends = []
waiter = False


def get_news():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://cat-fact.herokuapp.com" \
        "/facts/random?animal_type=cat&amount=1"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)

    return data['text']
