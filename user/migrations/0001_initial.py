# Generated by Django 2.1.1 on 2018-12-10 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField(choices=[(0, 'استوری'), (1, 'پست')], default=0, verbose_name='نوع')),
                ('photo', models.ImageField(blank=True, upload_to='', verbose_name='انتخاب عکس')),
                ('video', models.FileField(blank=True, upload_to='', verbose_name='انتخاب فیلم')),
                ('caption', models.CharField(blank=True, max_length=2200, null=True, verbose_name='کپشن')),
                ('uploaded_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='زمان آپلود فایل')),
                ('post_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان ارسال فایل')),
                ('sent', models.BooleanField(default=False, verbose_name='ارسال شده')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='شناسه اینستاگرام')),
                ('username', models.CharField(max_length=30, verbose_name='نام کاربری')),
                ('cookie', models.CharField(blank=True, default='', max_length=4000, null=True, verbose_name='کوکی')),
                ('phone_info', django_mysql.models.JSONField(blank=True, default=dict, null=True, verbose_name='اطلاعات دستگاه')),
                ('setting', django_mysql.models.JSONField(default=user.models.default_setting, verbose_name='تنظیمات')),
                ('json_chart', django_mysql.models.JSONField(default=dict)),
                ('live_activity', django_mysql.models.JSONField(default=user.models.default_live_activity, verbose_name='آخرین عملیات اکانت')),
                ('json_efficiency', django_mysql.models.JSONField(default=user.models.default_json_efficiency, verbose_name='بازدهی اکانت')),
                ('status', models.IntegerField(blank=True, default=-100, null=True, verbose_name='وضعیت')),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='زمان شروع فعالیت اکانت')),
                ('charge', models.IntegerField(blank=True, default=0, verbose_name='میزان شارژ باقی مانده')),
                ('first_time', models.BooleanField(default=True, verbose_name='اولین بار اضافه شده')),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='آخرین آپدیت یوزرنیم')),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('uid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='شناسه اینستاگرام')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='یوزر'),
        ),
    ]
