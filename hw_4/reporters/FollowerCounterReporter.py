import twitch
from Credentials import *

name = "FollowerCounterReporter"
version = "0.02"
depends = ['twitch']
waiter = False


def get_content(streamer):
    helix = twitch.Helix(Credentials.client_id, Credentials.secret_id)
    user = helix.user(streamer)
    return user.followers().total


def make_news(streamer, total_followers):
    title = f"У пользователя с ником {streamer} на данный момент \
{total_followers} подписчиков!"
    if total_followers < 1000:
        text = f"{streamer} на площадке twitch.tv собрал небольшое, \
но дружное сообщество из {total_followers} фолловеров на своём канале"
    elif total_followers < 100000:
        text = f"{streamer} c помощью площадки twitch смог заполучить \
немалую аудиторию размером {total_followers} фолловеров, благодаря \
своему таланту"
    elif total_followers < 1000000:
        text = f"{streamer} собрал целую армию из подписчиков, на него \
подписалось {total_followers} фолловеров Твиче, следим за его \
продвижением у миллиону!"
    else:
        text = f"{streamer} стал настоящей звездой, у него аж \
{total_followers} фолловеров на канале Твича, будем следить за его \
успехами и дальше!!!"

    return {
        'title': {title},
        'text': f'{text}'
    }


def get_news(streamer="bizzaretunez"):
    total_followers = get_content(streamer)
    return make_news(streamer, total_followers)


if __name__ == '__main__':
    print(get_news())
