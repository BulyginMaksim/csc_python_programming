from django.db import models
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    reporter_name = models.CharField(max_length=50)
    title = models.CharField(max_length=255, default='')
    text = models.TextField(default='')
    importance = models.FloatField(default=0)
    main_news = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("новость")
        verbose_name_plural = _("Новости")

    def __str__(self):
        return f"Новость: {self.title}. " \
               f"Время создания: {self.time}." \
               f"Репортер:{self.reporter_name}."


class Logs(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    reporter_name = models.CharField(max_length=50)
    log = models.TextField(default='')

    class Meta:
        verbose_name = _("лог")
        verbose_name_plural = _("Логи")

    def __str__(self):
        return f"Репортер {self.reporter_name} словил ошибку:{self.log}."
