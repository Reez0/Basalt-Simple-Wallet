from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging
logger = logging.getLogger("Celery")
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'basalt_simple_wallet.settings')

app = Celery('basalt_simple_wallet', broker="redis://broker:6379")
app.config_from_object('django.conf:settings',
                       namespace='basalt_simple_wallet')

app.autodiscover_tasks()
