"""
Репортер, который смотрит, выложили ли сегодня
очередное видео на некотором канале в YouTube.
Хотя это не сильно про новости, в принципе это может
быть полезно, чтобы отслеживать несколько каналов
в автоматическом режиме.
"""

from selenium import webdriver

name = "YouTubeMonitor"
version = "0.1"
depends = ["selenium"]
waiter = True


def get_url(channel_name):
    return f"https://www.youtube.com/c/{channel_name}/videos"


def is_posted_today(posted_str: str):
    return any([s in posted_str for s in ["hour", "minute", "second"]])


def get_news():
    channel_name_parameter = "zhizashow"
    url = get_url(channel_name_parameter)

    # the desired page is loaded dynamically,
    # so one solution is to use selenium
    driver = webdriver.Chrome()
    driver.get(url)

    # get full channel name from the page
    channel_name = driver.find_element_by_class_name(
        "style-scope ytd-channel-name"
    ).text

    # get info about the latest video
    elem_grid_rendered = driver.find_elements_by_class_name(
        "style-scope ytd-grid-renderer"
    )
    latest_video_info = elem_grid_rendered[0].text.split("\n")[:4]
    _, title, views_str, posted_str = latest_video_info

    if is_posted_today(posted_str):
        return {
            "title": f"Вперед смотреть {channel_name} - вышло новое видео!",
            "text": f"Уже {views_str.split()[0]} просмотров, а ты ещё не "
                    f"посмотрел?"
        }
