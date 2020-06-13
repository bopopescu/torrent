from django.core.management.base import BaseCommand

from torrent_main import models
from torrent import add_settings


class Command(BaseCommand):
    help = 'Creates groups'

    def handle(self, *args, **options):

        for category in add_settings.CATEGORIES:
            models.Category.objects.create(category_name=category)
        print('Done')
