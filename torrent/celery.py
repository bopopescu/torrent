import os
from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torrent.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'torrent.settings'

celery_app = Celery('torrent')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# search tasks.py-files in all apps
celery_app.autodiscover_tasks()

