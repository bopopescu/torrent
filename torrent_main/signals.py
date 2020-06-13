from django.dispatch import receiver
from django.db.models.signals import post_save
import logging

from torrent_main import models, tasks
from torrent_main.utils import parse_torrents


@receiver(post_save, sender=models.Torrent)
def parse_torrent_signal(sender, instance, created, **kwargs):
    id = instance.id
    tasks.parser.delay(id)
