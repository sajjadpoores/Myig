from django import template
import jdatetime
import datetime
from datetime import timedelta
import pytz

register = template.Library()


@register.filter(name='get_h_m_s')
def get_h_m_s(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return " {} روز و {} ساعت و {} دقیقه و {} ثانیه".format(d, h, m, s)


@register.filter(name='get_jalali')
def get_jalali(date):
    date = date.split('-')
    day = int(date[2])
    month = int(date[1])
    year = int(date[0])
    jdate = jdatetime.date.fromgregorian(day=day, month=month, year=year, locale='fa_IR')
    return jdate.strftime('%a, %d %b %Y')


@register.filter(name='get_times_ago')
def get_times_ago(ts_then):
    ts_now = int(datetime.datetime.now().timestamp())
    diff = ts_now - ts_then
    mins = diff // 60
    hours = mins // 60
    days = hours // 24
    months = days // 30
    years = months // 12

    if 0 <= diff <= 59:
        return "چند لحظه پیش"
    elif 1 <= mins <= 59:
        return "{} دقیقه پیش".format(mins)
    elif 1 <= hours <= 23:
        return "{} ساعت پیش".format(hours)
    elif 1 <= days <= 29:
        return "{} روز پیش".format(days)
    elif 1 <= months <= 11:
        return "{} ماه پیش".format(months)

    return "{} سال پیش".format(years)


@register.filter(name='to_jdatetime')
def to_jdatetime(dtime):
    jdatetime.set_locale("fa_IR")
    dtime = dtime + timedelta(hours=9, minutes=30)
    return jdatetime.datetime.fromgregorian(datetime=dtime).strftime("%a, %d %b %Y %H:%M:%S")


@register.filter(name='get_size')
def get_size(size):
    if size < 1024:
        return str(size) + ' B'
    elif 1024 <= size < 1024 * 1024:
        return str(size/1024) + ' KB'
    else:
        return str(size/(1024*1024)) + ' MB'
