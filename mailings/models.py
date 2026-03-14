from django.db import models
from django.utils.timezone import now

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена')
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    def update_status(self):
        current_time = now()
        if current_time < self.start_time:
            new_status = 'created'
        elif self.start_time <= current_time <= self.end_time:
            new_status = 'started'
        else:
            new_status = 'completed'

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

class Attempt(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка отправки'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    response = models.TextField(null=True, blank=True)
    mailing = models.ForeignKey(Mailing, related_name='attempts', on_delete=models.CASCADE)