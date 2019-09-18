from django.db import models
from client.models import Client
from django_mysql.models import JSONField
from django.utils import timezone
import json


def default_setting():
    setting = """
        {
            "like": {
                "mode": 2,
                "likes": [
                  0,
                  1000
                ],
                "comments": [
                  0,
                  1000
                ],
                "dontTryAgain": false,
                "likeAfterFlw": true
            },
            "post": {
                "caption": "",
                "copyPosts": false,
                "copyCaption": false
            },
            "tags": [
            {
              "pk": "موزیک",
              "mode": "tag",
              "text": "موزیک"
            },
            {
              "pk": "بازی",
              "mode": "tag",
              "text": "بازی"
            },
            {
              "pk": "خنده",
              "mode": "tag",
              "text": "خنده"
            },
            {
              "pk": "شاد",
              "mode": "tag",
              "text": "شاد"
            },
            {
              "pk": "کافه",
              "mode": "tag",
              "text": "کافه"
            },
            {
              "pk": "رستوران",
              "mode": "tag",
              "text": "رستوران"
            },
            {
              "pk": "تهران",
              "mode": "tag",
              "text": "تهران"
            },
            {
              "pk": "ماشین",
              "mode": "tag",
              "text": "ماشین"
            },
            {
              "pk": "باحال",
              "mode": "tag",
              "text": "باحال"
            },
            {
              "pk": "سلبریتی",
              "mode": "tag",
              "text": "سلبریتی"
            },
            {
              "pk": "فیلم",
              "mode": "tag",
              "text": "فیلم"
            },
            {
              "pk": "سریال",
              "mode": "tag",
              "text": "سریال"
            },
            {
              "pk": "ورزش",
              "mode": "tag",
              "text": "ورزش"
            },
            {
              "pk": "کامپیوتر",
              "mode": "tag",
              "text": "کامپیوتر"
            },
            {
              "pk": "موبایل",
              "mode": "tag",
              "text": "موبایل"
            },
            {
              "pk": "لپتاپ",
              "mode": "tag",
              "text": "لپتاپ"
            },
            {
              "pk": "دخترونه",
              "mode": "tag",
              "text": "دخترونه"
            },
            {
              "pk": "پسرونه",
              "mode": "tag",
              "text": "پسرونه"
            },
            {
              "pk": "خرید",
              "mode": "tag",
              "text": "خرید"
            },
            {
              "pk": "فروش",
              "mode": "tag",
              "text": "فروش"
            },
            {
              "pk": 1832385020352417,
              "mode": "location",
              "text": "تهران"
            },
            {
              "pk": 218047916,
              "mode": "location",
              "text": "تهران سعادت آباد"
            },
            {
              "pk": 331547983,
              "mode": "location",
              "text": "تهران پارس"
            },
            {
              "pk": 228761132,
              "mode": "location",
              "text": "برج میلاد"
            },
            {
              "pk": 751034485,
              "mode": "location",
              "text": "تبریز"
            },
            {
              "pk": 791699144,
              "mode": "location",
              "text": "اصفهان"
            },
            {
              "pk": 401962727,
              "mode": "location",
              "text": "اهواز"
            }
            ],
            "speed": 1,
            "direct": {
            "sendToAll": false,
            "messageList": [
              "ممنون که منو فالو کردی",
              "مرسی از فالو",
              "tnx",
              " با تشکر از فالو",
              "ممنو میشم پستامو ببینی ",
              "سپاس از فالو"
            ]
            },
            "follow": {
            "mode": 1,
            "posts": [
              5,
              100
            ],
            "flwers": [
              50,
              800
            ],
            "flwing": [
              100,
              5000
            ],
            "gender": 0,
            "hasPic": true,
            "limits": 20,
            "flwPublic": true,
            "flwPrivate": true,
            "dontTryAgain": true,
            "doseNotFlwBusiness": true
            },
            "comment": {
            "mode": 2,
            "likes": [
              0,
              1000
            ],
            "comments": [
              0,
              1000
            ],
            "commentList": [
              "لایک?",
              "عجب",
              "پستای جالبی داری",
              "واو",
              "?"
            ],
            "dontTryAgain": true,
            "commentAfterFlw": true
            },
            "flwFlag": true,
            "targets": [
            {
              "userId": 4524856086,
              "userName": "fun_tur"
            },
            {
              "userId": 8467344130,
              "userName": "whats.fact"
            },
            {
              "userId": 5541235123,
              "userName": "filmo__aks"
            },
            {
              "userId": 1645548032,
              "userName": "pandapry"
            },
            {
              "userId": 5549995570,
              "userName": "klonomi"
            },
            {
              "userId": 2957279578,
              "userName": "video4us"
            },
            {
              "userId": 3461763521,
              "userName": "angoorak.gp"
            },
            {
              "userId": 1511930500,
              "userName": "vocab.coding"
            },
            {
              "userId": 3287194632,
              "userName": "farsiart"
            },
            {
              "userId": 4279909378,
              "userName": "utube_farsi"
            },
            {
              "userId": 3408453717,
              "userName": "che.jaleeb"
            }
            ],
            "likeFlag": true,
            "unfollow": {
            "mode": 1,
            "time": 172800,
            "whiteList": [],
            "startFlwing": 500
            },
            "unflwFlag": true,
            "directFlag": false,
            "flwPerHour": 14,
            "commentFlag": false,
            "likePerHour": 20,
            "targetPosts": [],
            "commentsLike": {
            "mode": 3,
            "dontTryAgain": false
            },
            "unflwPerHour": 14,
            "directPerHour": 1,
            "commentPerHour": 5,
            "commentsLikeFlag": true,
            "commentsLikePerHour": 5
            }
        """

    setting = json.loads(setting)
    return setting


def default_live_activity():
    live_activity = '{ "data": []}'
    live_activity = json.loads(live_activity)
    return live_activity


def default_json_efficiency():
    json_efficiencty = '{"tags": [{"pk": "\u0645\u0634\u0647\u062f", "like": 0, "text": "\u0645\u0634\u0647\u062f", "count": 0, "follow": 0, "comment": 0}], "users": [{"pk": 1625416367, "like": 0, "count": 0, "follow": 0, "comment": 0, "userName": "balloonshop_badkonak"}, {"pk": 7860130871, "like": 0, "count": 0, "follow": 0, "comment": 0, "userName": "solo_tourism"}], "locations": [{"pk": 220592830, "like": 0, "text": "Mashhad, Iran", "count": 0, "follow": 0, "comment": 0}]}'
    json_efficiencty = json.loads(json_efficiencty)
    return json_efficiencty


class User(models.Model):
    uid = models.CharField(verbose_name='شناسه اینستاگرام', primary_key=True, max_length=20)
    cid = models.ForeignKey(Client, verbose_name='مشتری', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='نام کاربری', max_length=30, null=False, blank=False)
    cookie = models.CharField(verbose_name='کوکی', max_length=4000, null=True, blank=True, default="")
    phone_info = JSONField(verbose_name='اطلاعات دستگاه', null=True, blank=True)
    setting = JSONField(verbose_name='تنظیمات', null=False, blank=False, default=default_setting)
    json_chart = JSONField(null=False, blank=False)
    live_activity = JSONField(verbose_name='آخرین عملیات اکانت', null=False, blank=False, default=default_live_activity)
    json_efficiency = JSONField(verbose_name='بازدهی اکانت', null=False, blank=False, default=default_json_efficiency)
    status = models.IntegerField(verbose_name='وضعیت', null=True, default=-100, blank=True)
    start_time = models.DateTimeField(verbose_name='زمان شروع فعالیت اکانت', default=timezone.now, blank=True)
    charge = models.IntegerField(verbose_name='میزان شارژ باقی مانده', default=0, null=False, blank=True)
    first_time = models.BooleanField(verbose_name='اولین بار اضافه شده', default=True, null=False, blank=False)
    last_update = models.DateTimeField(verbose_name='آخرین آپدیت یوزرنیم', default=timezone.now, blank=False)

    def __str__(self):
        return self.username + ' - ' + str(self.cid) + ' - ' + str(self.uid)


class UserHistory(models.Model):
    uid = models.CharField(verbose_name='شناسه اینستاگرام', primary_key=True, max_length=20)


MODE_CHOICES = ((0, 'استوری'), (1, 'پست'))


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name='یوزر', on_delete=models.CASCADE)
    mode = models.IntegerField(verbose_name='نوع', blank=False, null=False, default=0, choices=MODE_CHOICES)
    photo = models.ImageField(verbose_name='انتخاب عکس', blank=True)
    video = models.FileField(verbose_name='انتخاب فیلم', blank=True)
    caption = models.CharField(verbose_name='کپشن', max_length=2200, blank=True, null=True)
    uploaded_at = models.DateTimeField(verbose_name='زمان آپلود فایل', default=timezone.now, blank=True, null=False)
    post_at = models.DateTimeField(verbose_name='زمان ارسال فایل', default=timezone.now, blank=False, null=False)
    sent = models.BooleanField(verbose_name='ارسال شده', default=False)

    def __str__(self):
        if self.mode == 0:
            return str(self.user.username) + ' - استوری - ' + str(self.uploaded_at)
        else:
            return str(self.user.username) + ' - پست - ' + str(self.uploaded_at)
