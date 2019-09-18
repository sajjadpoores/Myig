from django.db import models
from client.models import Client
from django.utils import timezone


class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='مشتری', null=False, blank=False)
    pic_url = models.CharField(verbose_name='تصویر', max_length=1024, blank=True, null=True)
    text = models.CharField(verbose_name='متن', max_length=1024, null=False, blank=False)
    type = models.IntegerField(verbose_name='نوع', null=False, blank=False)
    seen = models.BooleanField(verbose_name='دیده شده', null=False, blank=False, default=False)
    time = models.DateTimeField(verbose_name='زمان', null=False, blank=False, default=timezone.now)

    def __str__(self):
        return self.client.username + ' - ' + str(self.time)