from django.shortcuts import render
from django.http import HttpResponse
from miner.models import News


def index(request):
    news = News.objects.filter(main_news=0).order_by('-importance')
    main_news = News.objects.filter(main_news=1).order_by('-importance')
    if not main_news.count():
        # проверяем, есть ли какие-либо главные новости,
        # если нет, то говорим, что главной новостью будет первая
        # из обычных но с наибольшим importance
        main_news = news
    return render(request, 'index.html', {
        'news': news,
        'main_news': main_news
    })
