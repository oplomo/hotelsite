# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel.settings")

# Define the Celery application
app = Celery("hotel")

# Load task modules from all registered Django app configs.
app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule
# Autodiscover tasks
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print (f"request.{self.request}")
