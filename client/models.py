from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_mysql.models import JSONField


class Client(AbstractUser):
    username = models.CharField(verbose_name='نام کاربری', max_length=30, blank=False, unique=True)
    email = models.EmailField(verbose_name='ایمیل', blank=False, unique=True)
    marketer = models.BooleanField(verbose_name='بازاریاب', blank=False, default=False)
    used_free = models.BooleanField(verbose_name='از مدت رایگان استفاده کرده', blank=False, default=False)
    code = models.CharField(verbose_name='کد تایید', max_length=128, blank=True, null=True)
    parent = models.ForeignKey("self", verbose_name='معرف', null=True, on_delete=models.CASCADE, blank=True)
    participation = models.IntegerField(verbose_name='سود مشارکت', default=0, null=False)
    income = models.IntegerField(verbose_name='درآمد', default=0, null=False)
    activation_key = models.CharField(verbose_name='کد فعالسازی', max_length=40, blank=False, default="0")
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Activity(models.Model):
    cid = models.ForeignKey(Client, verbose_name='مشتری', blank=False, null=False, default=False, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='نام فعالیت', max_length=100, null=False, blank=False)
    detail = models.CharField(verbose_name='توضیحات فعالیت', max_length=500, null=True, blank=True)
    time = models.DateTimeField(verbose_name='زمان فعالیت', default=timezone.now, blank=True)

    def __str__(self):
        return str(self.cid) + ' - ' + self.activity + ' - ' + str(self.time)


class Plan(models.Model):
    name = models.CharField(verbose_name='نام پلن', max_length=128, blank=False, null=False)
    price = models.IntegerField(verbose_name='قیمت', blank=False, null=False)
    time = models.CharField(verbose_name='مدت زمان پلن', max_length=512, blank=False, null=False, default='')
    followers1 = models.IntegerField(verbose_name='حداقل تعداد افزایش فالوور', blank=False, null=False, default=0)
    followers2 = models.IntegerField(verbose_name='حداکثر تعداد افزایش فالوور', blank=False, null=False, default=0)
    charge = models.IntegerField(verbose_name='میزان شارژ', blank=False, null=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    cid = models.ForeignKey(Client, verbose_name='مشتری', blank=False, null=False, on_delete=models.CASCADE)
    pid = models.ForeignKey(Plan, verbose_name='پلن', blank=False, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='مبلغ', blank=False, null=False, default=False)
    done = models.BooleanField(verbose_name='انجام شده', default=False)
    items = JSONField(verbose_name='اقلام', null=False, blank=False)
    time = models.DateTimeField(verbose_name='زمان خرید', default=timezone.now, blank=True)

    def __str__(self):
        return self.cid.username + ' - ' + str(self.amount) + ' - ' + str(self.time)
