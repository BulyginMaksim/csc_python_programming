import twitch
import random
from Credentials import *

name = "StreamReporter"
version = "0.01"
depends = ['twitch']
waiter = True


class StreamerInfo:
    def __init__(self, streamer_name, user):
        self.name = streamer_name
        self.view_count = user.view_count
        self.stream_view_count = user.stream.viewer_count
        self.is_live = user.is_live


def get_content(streamer):
    helix = twitch.Helix(Credentials.client_id, Credentials.secret_id)
    user = helix.user(streamer)
    return StreamerInfo(streamer, user)


def make_news(streamer_info):
    if streamer_info.is_live:
        title = [
            f"{streamer_info.name} идёт смотреть ОНИМЕ!!",
            f"{streamer_info.name} включил стрим!!!",
            f"{streamer_info.name} подрубил!!!"
        ]
        status = 'Известный' \
            if streamer_info.view_count > 1000000 else 'Начинающий'

        body = [
            f"{status} стример с ником {streamer_info.name}"
            f"включил трансяцию на платформе twitch.tv.\n"
            f"На данный момент уже {streamer_info.stream_viewer_count} "
            f"пользователкей посмотрело трансляцию!"
            f"Скорей заходи!",

            f"{streamer_info.name} начал стримить по ссылке "
            f"twitch.tv/{streamer_info.name}!"
        ]

        return {'title': {random.choice(title)},
                'text': f'{random.choice(body)}'}


def get_news(streamer="bizzaretunez"):
    streamer_info = get_content(streamer)
    return make_news(streamer_info)


if __name__ == '__main__':
    print(get_news())
