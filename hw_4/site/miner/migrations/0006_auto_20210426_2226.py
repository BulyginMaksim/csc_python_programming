# Generated by Django 3.2 on 2021-04-26 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0005_alter_news_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logs',
            options={'verbose_name': 'лог', 'verbose_name_plural': 'Логи'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'новость', 'verbose_name_plural': 'Новости'},
        ),
    ]