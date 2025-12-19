import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_lookup.settings')

app = Celery('phone_lookup')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
