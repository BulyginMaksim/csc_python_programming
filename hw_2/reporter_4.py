from urllib.request import urlopen
import json
from datetime import datetime
import logging
import re


name = "ForecastRobot"
version = "1.00"
depends = ['datetime']
waiter = False

def get_news():
    try:
        url = "http://ws1.metcheck.com/ENGINE/v9_0/json.asp?lat=60.2&lon=30.3&lid=50517&Fc=No"
        data = urlopen(url).read().decode('utf8')
        data = json.loads(data)
    except Exception as e:
        return logging.warning(f'Произошла ошибка при парсинге: {e}')

    cur_hour = datetime.now().strftime("%H")
    cur_time = datetime.now().strftime("%H:%M")
    temperature, windspeed = 0, 0
    try:
        for d in data["metcheckData"]["forecastLocation"]["forecast"]:
            if re.findall("T\d+:", d["utcTime"])[0][1:-1] == cur_hour:
                temperature = d["temperature"]
                windspeed = round(float(d["windspeed"]) * 1.61, 2)
                break
    except Exception as e:
        return logging.warning(f'Произошла ошибка при поиске текущей погоды и скорости ветра: {e}')

    if temperature and windspeed:
        return {'title': f'{name} сообщает информацию о погоде в Санкт-Петербурге!',
                'text': f'На данный момент, в {cur_time} в Санкт-Петербурге {temperature}°С, '
                        f'а скорость ветра составляет {windspeed} километров в час!'}
    else:
        return f"На данный момент, в {cur_time} не была найдена информация о текущей погоде и (или) " \
               f"скорости ветра в Санкт-Петербурге."

print(get_news())