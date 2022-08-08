# D7_2
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_monday_8_hour': {
        'task': 'news.tasks.notify_subscribers_weekly',
        'schedule': crontab(), # Uncomment to test this feature
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

