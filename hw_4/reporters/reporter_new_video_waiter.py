from urllib.request import urlopen
import json

name = "RedRoomWaiter"
version = "0.1"
depends = ['datetime']
waiter = True


def get_news():
    from datetime import datetime
    url = "https://www.googleapis.com/youtube/v3" \
          "/search?key=(ваш ключ)&" \
          "channelId=UCsK1oV0PGkcZ1UhFtajx0dg&" \
          "part=snippet&" \
          "order=date&maxResults=5000"
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)

    last_video = data['items'][0]
    title = last_video['snippet']['title']

    published_time = last_video['snippet']['publishedAt']
    published_time = datetime.strptime(published_time, '%Y-%m-%dT%H:%M:%SZ')

    video_id = last_video['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    is_today = datetime.today().date() == published_time.date()
    if is_today:
        return {'title': f'на канале RedRoom вышло новое видео',
                'text': f' "{title}" уже на канале RedRoom. '
                        f'Посмотреть его можно по ссылке {video_url}'}
