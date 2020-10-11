import os

from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signals.settings.production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signals.settings.development')

app = Celery('signals')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
