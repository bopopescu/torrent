from django.apps import AppConfig


class TorrentMainConfig(AppConfig):
    name = 'torrent_main'

    def ready(self):
        import torrent_main.signals