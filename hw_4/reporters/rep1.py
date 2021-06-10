from urllib.request import urlopen

name = "TwitterBan"
version = "0.1"
depends = []
waiter = True


# Данный робожурналист ждет момент, когда в России заблокируют Twitter
def get_news():
    url = "https://twitter.com/"
    # url = "https://linkedin.com/"
    # url = "https://rutracker.org/"
    is_banned = False
    try:
        urlopen(url)
    except Exception:
        is_banned = True

    if is_banned:
        return {
            'title': f'Роскомнадзор смог заблокировать Twitter',
            'text': f'На территории России заблокирована социальная '
                    f'сеть Twitter. Редакция удостоверилась в том, '
                    f'что без использования VPN зайти на сайт {url} '
                    f'не представляется возможным.',
        }
    else:
        return None


# data = get_news()
# if data is not None:
#     print(data['title'])
#     print()
#     print(data['text'])
# else:
#     print('None')
