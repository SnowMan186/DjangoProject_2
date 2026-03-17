import os

from celery import Celery
from celery.schedules import crontab

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

app = Celery("mailing_service")

# Загружаем настройки из файла настроек Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживает задачи в приложениях Django
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-and-send-mailings": {
        "task": "mailings.tasks.check_and_send_mailings",
        "schedule": crontab(minute="*/5"),
    },
}
