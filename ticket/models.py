from django.db import models
from client.models import Client
from django.utils import timezone


class Ticket(models.Model):
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='فرستنده', null=False, blank=False)
    title = models.CharField(verbose_name='موضوع تیکت', max_length=256, null=False, blank=False)
    text = models.CharField(verbose_name='متن تیکت', max_length=1024, null=False, blank=False)
    attachment = models.ImageField(verbose_name='پیوست', null=True, blank=True)
    reply = models.CharField(verbose_name='پاسخ', max_length=1024, null=True, blank=True, default='')
    seen = models.BooleanField(verbose_name='دیده شده', null=False, blank=False, default=False)
    replied = models.BooleanField(verbose_name='پاسخ داده شده', null=False, blank=False, default=False)
    sent_time = models.DateTimeField(verbose_name='زمان ارسال', null=False, blank=False, default=timezone.now)
    replied_time = models.DateTimeField(verbose_name='زمان ارسال پاسخ', null=False, blank=False, default=timezone.now)

    def __str__(self):
        return self.sender.username + ' - ' + self.title
