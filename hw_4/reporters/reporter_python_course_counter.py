from urllib.request import urlopen
import json

name = "PythonCourseCounter"
version = "0.1"
depends = []
waiter = False


def get_news():
    url = "https://www.googleapis.com/youtube/v3/playlistItems?" \
          "part=snippet&playlistId=PLlb7e2G7aSpQmGnhrxlqI4iMXNv4R7khy&" \
          "maxResults=50&order=date&type=video&key=ключ"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)

    last_lection = data['items'][-1]
    title = last_lection['snippet']['title']
    video_id = last_lection['snippet']['resourceId']['videoId']
    video_url = f'https://www.googleapis.com/youtube/v3/videos?' \
                f'part=statistics&id={video_id}&' \
                f'key=<insert you key>'

    video_data = urlopen(video_url).read().decode('utf8')
    video_data = json.loads(video_data)
    video_counts = video_data['items'][0]['statistics']['viewCount']

    return f'Последнюю лекцию "{title}" курса "Программирование на Python" ' \
           f'посмотрели {video_counts} раз. '
