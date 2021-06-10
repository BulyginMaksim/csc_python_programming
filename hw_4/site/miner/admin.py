from django.contrib import admin
from .models import News, Logs


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('time', 'reporter_name',
                    'title',
                    'importance',
                    'main_news')
    list_filter = ('reporter_name',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('reporter_name', 'log')
    list_filter = ('reporter_name',)
