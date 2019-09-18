from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from client.views import get_client
from user.views import get_insta_info, get_insta_info2, get_user
from .models import Notification
from django.http import JsonResponse
from django.core import serializers
from client.templatetags.tags import get_times_ago
import datetime
import json


class AddFollowBackView(TemplateView):

    def get(self, request, fuid, tuid):
        fuser = get_user(fuid)
        tuser = get_insta_info2(tuid)

        if not fuser:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        text = '{} اکانت {} را فالو کرد.'.format(tuser['username'], fuser.username)
        client = fuser.cid
        notification = Notification(client=client, text=text, type=0)
        notification.save()

        return HttpResponse('done!')


class GetFollowBacksView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and request.user == client):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notifications = Notification.objects.filter(client=client, type=0)
        output = serializers.serialize('json', notifications)
        output = json.loads(output)

        i = 0
        for notification in notifications:
            dtime = notification.time
            ts_then = dtime.strftime('%s')
            output[i]['timestamp'] = get_times_ago(int(ts_then))
            i = i + 1

        return JsonResponse(output, safe=False)


def get_notification(cid):
    try:
        notification = Notification.objects.get(pk=cid)
    except Notification.DoesNotExist:
        notification = None
    return notification


class DeleteFollowBackView(TemplateView):

    def get(self, request, cid, nid):
        client = get_client(cid)
        notification = get_notification(nid)

        if not (client and request.user == client and notification and notification.client == request.user):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notification.delete()

        return HttpResponse('done!')


class AddBlockNotificationView(TemplateView):

    def get(self, request, uid, type):
        user = get_user(uid)
        if user:
            client = user.cid
        else:
            return HttpResponse("There is no such user!")

        user_info = get_insta_info(user.username)

        if not (client and user):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if type == 1:
            text = 'فالو اکانت {} بلاک شده است.'.format(user.username)
        elif type == 2:
            text = 'لایک اکانت {} بلاک شده است.'.format(user.username)
        elif type == 3:
            text = 'کامنت اکانت {} بلاک شده است.'.format(user.username)
        elif type == 4:
            text = 'آنفالو اکانت {} بلاک شده است.'.format(user.username)
        else:
            return HttpResponse("wrong notification type")  # TODO: redirect to error page

        notification = Notification.objects.filter(text=text, type=type)
        if notification:
            notification = notification[0]
            notification.text = text
            notification.seen = False
            notification.time = datetime.datetime.now()
            notification.pic_url = user_info['profile_pic_url']
        else:
            notification = Notification(client=client, text=text, type=type, pic_url=user_info['profile_pic_url'])

        notification.save()
        return HttpResponse('done!')


class GetBlockNotificationView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and request.user == client):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notifications = Notification.objects.filter(client=client).exclude(type=0).exclude(type=5)
        output = serializers.serialize('json', notifications)
        output = json.loads(output)

        i = 0
        for notification in notifications:
            dtime = notification.time
            ts_then = dtime.strftime('%s')
            output[i]['timestamp'] = get_times_ago(int(ts_then))
            i = i + 1

        return JsonResponse(output, safe=False)


class SeenBlockNotificationView(TemplateView):

    def get(self, request, cid, nid):
        client = get_client(cid)
        notification = get_notification(nid)

        if not (client and request.user == client and notification and notification.client == request.user):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notification.seen = True
        notification.save()

        return HttpResponse('done!')


class GetTicketNotificationView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and request.user == client):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notifications = Notification.objects.filter(client=client, type=5)
        output = serializers.serialize('json', notifications)
        output = json.loads(output)

        i = 0
        for notification in notifications:
            dtime = notification.time
            ts_then = dtime.strftime('%s')
            output[i]['timestamp'] = get_times_ago(int(ts_then))
            i = i + 1

        return JsonResponse(output, safe=False)


class GetTicketAndBlockNotificationView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and request.user == client):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        notifications = Notification.objects.filter(client=client).exclude(type=0).order_by('time')
        output = serializers.serialize('json', notifications)
        output = json.loads(output)

        i = 0
        for notification in notifications:
            dtime = notification.time
            ts_then = dtime.strftime('%s')
            output[i]['timestamp'] = get_times_ago(int(ts_then))
            i = i + 1

        return JsonResponse(output, safe=False)