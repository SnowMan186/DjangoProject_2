from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Attempt, Mailing
from .utils import send_message


@shared_task
def check_and_send_mailings():
    """
    Задача для регулярного запуска проверок рассылок.
    """
    current_time = timezone.now()
    active_mailings = Mailing.objects.filter(
        start_time__lte=current_time, end_time__gte=current_time
    )
    for mailing in active_mailings:
        send_message.delay(mailing.pk)


@shared_task
def send_message(mailing_pk):
    mailing = Mailing.objects.get(pk=mailing_pk)
    message = mailing.message
    for recipient in mailing.recipients.all():
        send_mail(
            message.subject,
            message.body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
        )
        Attempt.objects.create(
            status="Sent", response=f"Sent to {recipient.email}", mailing=mailing
        )
