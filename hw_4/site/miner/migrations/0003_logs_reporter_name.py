# Generated by Django 3.2 on 2021-04-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0002_auto_20210425_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='reporter_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
