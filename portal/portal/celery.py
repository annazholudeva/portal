import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mail_every_monday_8am': {
        'task': 'news.tasks.weekly_news',
        'schedule': crontab(hour=15, minute=40, day_of_week='tuesday'),
    },
}
