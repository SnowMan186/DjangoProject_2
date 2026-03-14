from celery import task
from .models import Mailing
from .utils import send_message

@task
def check_and_send_mailings():
    """
    Задача для регулярного запуска проверок рассылок.
    """
    current_time = timezone.now()
    mailings = Mailing.objects.filter(status='started')

    for mailing in mailings:
        if mailing.start_time <= current_time <= mailing.end_time:
            message = mailing.message
            for recipient in mailing.recipients.all():
                send_message(recipient.email, message.subject, message.body)