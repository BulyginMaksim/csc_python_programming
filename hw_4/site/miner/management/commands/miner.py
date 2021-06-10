from django.core.management.base import BaseCommand, CommandError
from miner.miner_app import mine


class Command(BaseCommand):
    help = 'Данная команда активирует майнер'

    def handle(self, *args, **options):
        mine()
