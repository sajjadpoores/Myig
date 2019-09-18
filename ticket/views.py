from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from client.views import get_client
from .forms import TicketCreateForm
from .models import Ticket
import datetime
from notification.models import Notification
from client.models import Client


class TicketAddView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = TicketCreateForm()

        return render(request, 'ticket/create.html', {'form': form})

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(client)
            admins = Client.objects.filter(is_staff=True)
            for admin in admins:
                notification = Notification(client=admin, text='شما یک تیکت جدید دارید.', type=5)
                notification.save()
            return redirect('/ticket/{}/list'.format(cid))
        return render(request, 'ticket/create.html', {'form': form})


class TicketListView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and request.user == client):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if request.user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(sender=client)

        # delete ticket notifications of this client
        # notifications = Notification.objects.filter(client=client, type=5)
        # for notification in notifications:
        #     notification.delete()

        return render(request, 'ticket/list.html', {'tickets': tickets})


class TicketUnseenListView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        tickets = Ticket.objects.filter(seen=False)

        # delete ticket notifications of this client
        notifications = Notification.objects.filter(client=request.user, type=5)
        for notification in notifications:
            notification.delete()
        return render(request, 'ticket/list.html', {'tickets': tickets})


class TicketUnrepliedListView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        tickets = Ticket.objects.filter(replied=False)

        # delete ticket notifications of this client
        notifications = Notification.objects.filter(client=request.user, type=5)
        for notification in notifications:
            notification.delete()
        return render(request, 'ticket/list.html', {'tickets': tickets})


def get_ticket(tid, hidden=False):
    try:
        ticket = Ticket.objects.get(pk=tid)
        if hidden and not ticket.seen:
            ticket.seen = True
            ticket.save()
    except Ticket.DoesNotExist:
        ticket= None
    return ticket


class TicketReplyView(TemplateView):

    def get(self, request, tid):
        ticket = get_ticket(tid, True)
        if not (ticket and request.user.is_staff):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        error = ''
        if ticket.replied:
            error = 'به این تیکت پاسخ داده اید. در صورت ارسال پاسخ مجدد، پاسخ جدید جایگزین خواهد شد.'
        return render(request, 'ticket/reply.html', {'ticket': ticket, 'error': error})

    def post(self, request, tid):
        ticket = get_ticket(tid, True)
        if not (ticket and request.user.is_staff):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        reply = request.POST.get('reply', None)
        if reply and len(reply) >= 10:
            ticket.replied = True
            ticket.reply = reply
            ticket.replied_time = datetime.datetime.now()
            ticket.save()
            notification = Notification(client=ticket.sender, text='یک پیام جدید دارید.', type=5)
            notification.save()
            return redirect('/ticket/{}/list/'.format(request.user.id))  # TODO: redirect to unreplied view

        return render(request, 'ticket/reply.html', {'ticket': ticket, 'error': 'متن پاسخ کمتر از ۱۰ کاراکتر است.'})


class TicketDetailView(TemplateView):

    def get(self, request, cid, tid):
        client = get_client(cid)
        if request.user.is_staff:
            ticket = get_ticket(tid, True)
        else:
            ticket = get_ticket(tid)

        if not (ticket and client and (request.user == client == ticket.sender or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'ticket/detail.html', {'ticket': ticket})
