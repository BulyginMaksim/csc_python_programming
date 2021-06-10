from urllib.request import urlopen
import json
import ssl


name = "NataZen"
version = "0.1"
depends = []
waiter = True


def get_news():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://www.metaweather.com/api/location/2123260"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    if data['consolidated_weather'][0]['weather_state_name'] in \
            ('Clear', 'Light Cloud'):
        return "Uraaa! It's sunny in St. Petersburg!"
    else:
        return None


if __name__ == '__main__':
    print(get_news())
