from __future__ import absolute_import, unicode_literals

from torrent.celery import celery_app
from torrent_main.utils.parse_torrents import TorrentParser
from datetime import datetime
from celery.app.task import Task
import socket

from torrent_main import models


class BaseSaver():

    def __init__(self, torrent):
        self.torrent = torrent

    def save_to_base(self, data):
        self.torrent.total_size = data['full_size']
        self.torrent.last_checked = datetime.now()
        self.torrent.seeders = data['info']['seeds']
        self.torrent.leeches = data['info']['leeches']
        self.torrent.info_hash = data['info_hash']
        self.torrent.is_pub = True
        for file in data['files']:
            models.TorrentFileInfo.objects.create(size=file['size'],
                                                  name=file['name'],
                                                  torrent=self.torrent)
        self.torrent.save()


class TorrentParserTask(Task):
    name = 'Parse torrent'
    max_retries = 5
    acks_late = True
    default_retry_delay = 5

    def run(self, torrent_id=None):
        self.torrent = models.Torrent.objects.get(id=torrent_id)

        if self.torrent.is_pub:
            return

        file_path = self.torrent.file.path

        parser = TorrentParser(file_path)
        try:
            res = parser.run()
        except socket.timeout:
            self.retry()

        saver = BaseSaver(self.torrent)
        saver.save_to_base(res)
        return res


parser = celery_app.register_task(TorrentParserTask())
