from django.conf import settings
from django.core.mail import send_mail

from .models import Attempt


def send_message(recipient, subject, body, mailing):
    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [recipient])
        Attempt.objects.create(status="sent", mailing=mailing)
    except Exception as e:
        Attempt.objects.create(status="failed", response=str(e), mailing=mailing)
